import os
import pty
import asyncio
import fcntl
import termios
import struct
import subprocess
from typing import Set
from fastapi import WebSocket

class TerminalSessionManager:
    """
    Persistent PTY Session Manager with an in-memory ring-buffer replay log.
    Ensures that browser page reloads, tab switches, and network reconnects
    do NOT terminate running bash processes or drop command outputs.
    """
    def __init__(self, cwd="/ansible", buffer_size=256 * 1024):
        self.cwd = cwd
        self.buffer_size = buffer_size
        self.buffer = bytearray()
        self.master_fd = None
        self.proc = None
        self.subscribers: Set[WebSocket] = set()
        self.read_task = None
        self.lock = asyncio.Lock()

    def is_alive(self) -> bool:
        return (
            self.proc is not None
            and self.proc.poll() is None
            and self.master_fd is not None
        )

    def _init_pty(self):
        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self.master_fd = None

        if self.proc is not None and self.proc.poll() is None:
            try:
                self.proc.terminate()
            except OSError:
                pass
            self.proc = None

        master_fd, slave_fd = pty.openpty()

        try:
            attrs = termios.tcgetattr(slave_fd)
            attrs[3] |= (termios.ECHO | termios.ICANON | termios.ECHOE | termios.ECHOK | termios.ISIG | termios.IEXTEN)
            termios.tcsetattr(slave_fd, termios.TCSANOW, attrs)
        except Exception:
            pass

        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        env["COLORTERM"] = "truecolor"
        env["HOME"] = os.path.expanduser("~")
        env["USER"] = os.getenv("USER", "root")
        env["PATH"] = os.getenv("PATH", "/usr/local/bin:/usr/bin:/bin")
        env["HISTFILE"] = os.path.join(self.cwd, ".lab_bash_history")
        env["HISTSIZE"] = "10000"
        env["HISTFILESIZE"] = "20000"
        env["PROMPT_COMMAND"] = "stty echo icanon 2>/dev/null; history -a"
        env["PAGER"] = "less -R -F -X"
        env["LESS"] = "-R -F -X"

        # Start interactive login bash in target project directory
        target_cwd = self.cwd if os.path.exists(self.cwd) else os.getcwd()
        proc = subprocess.Popen(
            ["/bin/bash", "--login", "-i"],
            preexec_fn=os.setsid,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=target_cwd,
            env=env
        )
        os.close(slave_fd)

        fl = fcntl.fcntl(master_fd, fcntl.F_GETFL)
        fcntl.fcntl(master_fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        self.master_fd = master_fd
        self.proc = proc

        # Cancel any previous reader task
        if self.read_task and not self.read_task.done():
            self.read_task.cancel()

        # Launch background async reader
        self.read_task = asyncio.create_task(self._read_loop())

    async def _read_loop(self):
        while self.is_alive():
            await asyncio.sleep(0.015)
            try:
                data = os.read(self.master_fd, 4096)
                if not data:
                    break

                # Append to rolling ring buffer
                self.buffer.extend(data)
                if len(self.buffer) > self.buffer_size:
                    overflow = len(self.buffer) - self.buffer_size
                    del self.buffer[:overflow]

                # Broadcast to all connected WebSockets
                dead_sockets = set()
                for ws in list(self.subscribers):
                    try:
                        await ws.send_bytes(data)
                    except Exception:
                        dead_sockets.add(ws)

                for dead in dead_sockets:
                    self.subscribers.discard(dead)

            except (BlockingIOError, InterruptedError):
                continue
            except OSError:
                break
            except Exception:
                break

        # Process exited or died
        if self.proc and self.proc.poll() is not None:
            self.proc = None

    async def register_client(self, websocket: WebSocket):
        async with self.lock:
            if not self.is_alive():
                self._init_pty()

            self.subscribers.add(websocket)

            # Replay captured buffer so newly connected client sees exact state
            if self.buffer:
                try:
                    await websocket.send_bytes(bytes(self.buffer))
                except Exception:
                    self.subscribers.discard(websocket)

    def unregister_client(self, websocket: WebSocket):
        self.subscribers.discard(websocket)

    def write_input(self, data: bytes):
        if self.is_alive():
            try:
                os.write(self.master_fd, data)
            except OSError:
                pass

    def resize_pty(self, cols: int, rows: int):
        cols = max(int(cols or 80), 20)
        rows = max(int(rows or 24), 5)
        if self.is_alive():
            try:
                winsize = struct.pack("HHHH", rows, cols, 0, 0)
                fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
            except OSError:
                pass

    def reset_session(self):
        """Forces a clean restart of the PTY session."""
        self.buffer.clear()
        self._init_pty()

# Global singleton session instance
session_manager = TerminalSessionManager()
