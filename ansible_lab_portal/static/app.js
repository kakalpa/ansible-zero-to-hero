let curriculum = null;
let currentExercise = null;
let currentLearningMode = localStorage.getItem('ansible_learning_mode') || 'guided';
let currentLessonStep = 'primer';

// Terminal globals
let term = null;
let fitAddon = null;
let termSocket = null;
let activeTab = 'terminal';
let toastTimeout = null;

// DOM Elements
const appLayout = document.getElementById('app-layout');
const btnToggleSidebar = document.getElementById('btn-toggle-sidebar');
const curriculumList = document.getElementById('curriculum-list');
const exerciseBreadcrumb = document.getElementById('exercise-breadcrumb');
const exerciseTitlePill = document.getElementById('exercise-title-pill');
const exerciseTicket = document.getElementById('exercise-ticket');
const exerciseTitle = document.getElementById('exercise-title');
const exerciseTags = document.getElementById('exercise-tags');
const scenTargetChip = document.getElementById('scen-target-chip');
const objectiveContent = document.getElementById('objective-content');
const tasksChecklist = document.getElementById('tasks-checklist');
const btnPeekNode = document.getElementById('btn-peek-node');
const inspectOutput = document.getElementById('inspect-output');
const inspectCmdLabel = document.getElementById('inspect-cmd-label');

// Two-Stage Learning DOM
const learningModeSwitcher = document.getElementById('learning-mode-switcher');
const modeGuided = document.getElementById('mode-guided');
const modeChallenge = document.getElementById('mode-challenge');
const lessonStepNav = document.getElementById('lesson-step-nav');
const btnStepPrimer = document.getElementById('btn-step-primer');
const btnStepChallenge = document.getElementById('btn-step-challenge');
const stepPanePrimer = document.getElementById('step-pane-primer');
const stepPaneChallenge = document.getElementById('step-pane-challenge');
const btnAdvanceChallenge = document.getElementById('btn-advance-challenge');
const btnBackToPrimer = document.getElementById('btn-back-to-primer');
const btnCopyBlueprint = document.getElementById('btn-copy-blueprint');
const btnInsertBlueprint = document.getElementById('btn-insert-blueprint');
const btnInsertBlueprintLabel = document.getElementById('btn-insert-blueprint-label');
const accordionGuide = document.getElementById('accordion-guide');
const accordionHints = document.getElementById('accordion-hints');
const accordionTargetState = document.getElementById('accordion-target-state');
const guideXpBadge = document.getElementById('guide-xp-badge');
const hintsXpBadge = document.getElementById('hints-xp-badge');
const guideContent = document.getElementById('guide-content');
const hintsContainer = document.getElementById('hints-container');
const btnRevealSolution = document.getElementById('btn-reveal-solution');
const solutionWrapper = document.getElementById('solution-wrapper');
const solutionCodeView = document.getElementById('solution-code-view');
const terminalOutput = document.getElementById('terminal-output');
const terminalStatus = document.getElementById('terminal-status');
const valBadgeChip = document.getElementById('val-badge-chip');
const valDetails = document.getElementById('val-details');
const btnMaximizeTerm = document.getElementById('btn-maximize-term');
const maxTermIcon = document.getElementById('max-term-icon');

// Gamification HUD DOM
const hudRankIcon = document.getElementById('hud-rank-icon');
const hudRankName = document.getElementById('hud-rank-name');
const hudXpAmount = document.getElementById('hud-xp-amount');
const hudXpPill = document.getElementById('hud-xp-pill');
const hudStreakCount = document.getElementById('hud-streak-count');
const hudTimerPill = document.getElementById('hud-timer-pill');
const hudTimerVal = document.getElementById('hud-timer-val');
const btnOpenBadges = document.getElementById('btn-open-badges');
const hudBadgeCount = document.getElementById('hud-badge-count');
const confettiCanvas = document.getElementById('confetti-canvas');

// Tabs, Editor & Toast DOM
const tabBtnTerminal = document.getElementById('tab-btn-terminal');
const tabBtnEditor = document.getElementById('tab-btn-editor');
const tabBtnSplit = document.getElementById('tab-btn-split');
const tabBtnResults = document.getElementById('tab-btn-results');
const viewTerminal = document.getElementById('view-terminal');
const viewEditor = document.getElementById('view-editor');
const viewResults = document.getElementById('view-results');
const splitPaneResizer = document.getElementById('split-pane-resizer');
const executionPanel = document.getElementById('execution-panel');

const editorActiveFilename = document.getElementById('editor-active-filename');
const btnEditorSave = document.getElementById('btn-editor-save');
const btnEditorRun = document.getElementById('btn-editor-run');
const btnEditorRunText = document.getElementById('btn-editor-run-text');
const btnEditorRunIcon = document.getElementById('btn-editor-run-icon');
const btnEditorRunDropdown = document.getElementById('btn-editor-run-dropdown');
const runOptionsMenu = document.getElementById('run-options-menu');
const btnFlagCheck = document.getElementById('btn-flag-check');
const btnFlagDiff = document.getElementById('btn-flag-diff');

const resultFloatingToast = document.getElementById('result-floating-toast');
const toastIcon = document.getElementById('toast-icon');
const toastMsg = document.getElementById('toast-msg');
const btnToastViewResults = document.getElementById('btn-toast-view-results');
const btnToastNextLesson = document.getElementById('btn-toast-next-lesson');
const btnNextExercise = document.getElementById('btn-next-exercise');
const btnNextLessonResults = document.getElementById('btn-next-lesson-results');

const btnValidate = document.getElementById('btn-validate-exercise');
const btnReset = document.getElementById('btn-reset-exercise');
const btnCopySolution = document.getElementById('btn-copy-solution');
const btnPasteTerminal = document.getElementById('btn-paste-terminal');
const btnOpenSettings = document.getElementById('btn-open-settings');
const btnCloseSettings = document.getElementById('btn-close-settings');
const modalSettings = document.getElementById('modal-settings');
const clusterTableBody = document.getElementById('cluster-table-body');
const btnFullRollback = document.getElementById('btn-full-rollback');
const rollbackStatus = document.getElementById('rollback-status');

// Progress DOM
const userProgressText = document.getElementById('user-progress-text');
const userProgressBar = document.getElementById('user-progress-bar');
const userProgressAria = document.getElementById('user-progress-aria');

// Resizer DOM
const workspaceGrid = document.getElementById('workspace-grid');
const instructionPanel = document.getElementById('instruction-panel');
const workspaceResizer = document.getElementById('workspace-resizer');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  initTerminal();
  initCodeEditor();
  initAudioSynthesizer();
  setupSidebarToggle();
  setupPlaygroundTabs();
  setupNextLessonButtons();
  setupSettingsModal();
  setupBadgesModal();
  setupRepoExport();
  setupExecutionActions();
  setupScenarioFeatures();
  setupWorkspaceResizer();
  setupKeyboardShortcuts();
  setupLearningModeSwitcher();
  setupLessonStepNav();
  await loadCurriculum();
  updateProgressTracker();
  initFleetTelemetryStream();
  setupFleetTopologyToggle();
});

// Interactive xterm.js Terminal Setup
function initTerminal() {
  const container = document.getElementById('xterm-container');
  if (!container || term) return;

  term = new Terminal({
    cursorBlink: true,
    fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace',
    fontSize: 13,
    lineHeight: 1.25,
    theme: {
      background: '#090d12',
      foreground: '#c9d1d9',
      cursor: '#6366f1',
      selectionBackground: 'rgba(99, 102, 241, 0.35)',
      black: '#484f58',
      red: '#f43f5e',
      green: '#10b981',
      yellow: '#f59e0b',
      blue: '#6366f1',
      magenta: '#a855f7',
      cyan: '#06b6d4',
      white: '#f1f5f9'
    }
  });

  fitAddon = new FitAddon.FitAddon();
  term.loadAddon(fitAddon);
  term.open(container);

  container.addEventListener('click', () => {
    if (term) term.focus();
  });

  setTimeout(() => {
    if (fitAddon) fitAddon.fit();
    if (term) term.focus();
  }, 120);

  connectTerminalWebSocket();
}

function connectTerminalWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const url = `${protocol}//${window.location.host}/ws/terminal`;
  termSocket = new WebSocket(url);
  termSocket.binaryType = 'arraybuffer';

  termSocket.onopen = () => {
    setTerminalStatus('online', 'Shell Connected');
    sendTerminalResize();
  };

  termSocket.onmessage = (event) => {
    if (typeof event.data === 'string') {
      term.write(event.data);
    } else {
      term.write(new Uint8Array(event.data));
    }
  };

  termSocket.onclose = () => {
    setTerminalStatus('offline', 'Shell Disconnected');
    term.write('\r\n\x1b[31m[Shell disconnected. Press any key to reconnect]\x1b[0m\r\n');
  };

  term.onData(data => {
    if (termSocket && termSocket.readyState === WebSocket.OPEN) {
      termSocket.send(JSON.stringify({ type: 'input', data }));
    } else if (termSocket && termSocket.readyState === WebSocket.CLOSED) {
      connectTerminalWebSocket();
    }
  });

  window.addEventListener('resize', () => {
    if (fitAddon) {
      fitAddon.fit();
      sendTerminalResize();
    }
  });
}

function sendTerminalResize() {
  if (termSocket && termSocket.readyState === WebSocket.OPEN && term) {
    const cols = Math.max(term.cols || 80, 20);
    const rows = Math.max(term.rows || 24, 5);
    termSocket.send(JSON.stringify({
      type: 'resize',
      cols: cols,
      rows: rows
    }));
  }
}

function sendStringToTerminal(str) {
  if (termSocket && termSocket.readyState === WebSocket.OPEN) {
    termSocket.send(JSON.stringify({ type: 'input', data: str }));
    if (term) term.focus();
  }
}

// Clear Terminal Viewport and Reset Interactive Shell Prompt
function clearTerminalShell() {
  if (term) {
    try {
      term.write('\x1b[2J\x1b[3J\x1b[H');
      term.clear();
    } catch (e) {
      console.warn('Failed to clear terminal buffer:', e);
    }
  }

  if (termSocket && termSocket.readyState === WebSocket.OPEN) {
    try {
      // Abort any pending command or pager (Ctrl+C, q)
      termSocket.send(JSON.stringify({ type: 'input', data: '\x03\x03q\r\x03' }));
      setTimeout(() => {
        if (termSocket && termSocket.readyState === WebSocket.OPEN) {
          // Send stty sane to guarantee ECHO is restored, then clear
          termSocket.send(JSON.stringify({ type: 'input', data: 'stty sane 2>/dev/null; clear\r' }));
        }
        if (term) {
          try {
            term.clear();
            term.focus();
          } catch (e) {}
        }
      }, 70);
    } catch (err) {
      console.warn('Failed to send clear command over terminal socket:', err);
    }
  }
}

// Sidebar Toggle
function setupSidebarToggle() {
  if (btnToggleSidebar && appLayout) {
    btnToggleSidebar.addEventListener('click', () => {
      appLayout.classList.toggle('sidebar-collapsed');
      setTimeout(() => {
        if (fitAddon) {
          fitAddon.fit();
          sendTerminalResize();
        }
      }, 260);
    });
  }
}

// Playground Tabs & Dual Workspace Layout
function setupPlaygroundTabs() {
  if (tabBtnTerminal) tabBtnTerminal.addEventListener('click', () => switchTab('terminal'));
  if (tabBtnEditor) tabBtnEditor.addEventListener('click', () => switchTab('editor'));
  if (tabBtnSplit) tabBtnSplit.addEventListener('click', () => switchTab('split'));
  if (tabBtnResults) tabBtnResults.addEventListener('click', () => switchTab('results'));

  if (btnToastViewResults) {
    btnToastViewResults.addEventListener('click', () => {
      switchTab('results');
      hideFloatingToast();
    });
  }
}

function switchTab(tab) {
  // If user tries to open editor or split view on an exercise that doesn't use playbooks, lock to terminal
  if ((tab === 'editor' || tab === 'split') && (!currentExercise || !currentExercise.target_file)) {
    tab = 'terminal';
  }

  activeTab = tab;

  [tabBtnTerminal, tabBtnEditor, tabBtnSplit, tabBtnResults].forEach(btn => {
    if (btn) btn.classList.remove('active');
  });

  if (executionPanel) {
    executionPanel.classList.remove('layout-split');
  }
  if (splitPaneResizer) {
    splitPaneResizer.style.display = 'none';
  }

  if (tab === 'terminal') {
    if (tabBtnTerminal) tabBtnTerminal.classList.add('active');
    if (viewTerminal) viewTerminal.style.display = 'flex';
    if (viewEditor) viewEditor.style.display = 'none';
    if (viewResults) viewResults.style.display = 'none';
    setTimeout(() => {
      if (fitAddon) {
        fitAddon.fit();
        sendTerminalResize();
      }
      if (term) term.focus();
    }, 50);
  } else if (tab === 'editor') {
    if (tabBtnEditor) tabBtnEditor.classList.add('active');
    if (viewTerminal) viewTerminal.style.display = 'none';
    if (viewEditor) viewEditor.style.display = 'flex';
    if (viewResults) viewResults.style.display = 'none';
    setTimeout(() => {
      if (codeEditor) {
        codeEditor.refresh();
        codeEditor.focus();
      }
    }, 50);
  } else if (tab === 'split') {
    if (tabBtnSplit) tabBtnSplit.classList.add('active');
    if (executionPanel) executionPanel.classList.add('layout-split');
    if (viewTerminal) viewTerminal.style.display = 'flex';
    if (viewEditor) viewEditor.style.display = 'flex';
    if (viewResults) viewResults.style.display = 'none';
    if (splitPaneResizer) splitPaneResizer.style.display = 'block';
    setTimeout(() => {
      if (codeEditor) codeEditor.refresh();
      if (fitAddon) {
        fitAddon.fit();
        sendTerminalResize();
      }
    }, 50);
  } else if (tab === 'results') {
    if (tabBtnResults) tabBtnResults.classList.add('active');
    if (viewTerminal) viewTerminal.style.display = 'none';
    if (viewEditor) viewEditor.style.display = 'none';
    if (viewResults) viewResults.style.display = 'flex';
    hideFloatingToast();
  }
}

// ==========================================================
// CODE EDITOR (CODEMIRROR) & SCOPED LESSON FILE CONTROLLER
// ==========================================================
let codeEditor = null;
let currentEditingPath = '';
let isEditorDirty = false;

function initCodeEditor() {
  const textarea = document.getElementById('playbook-editor-textarea');
  if (!textarea || codeEditor || typeof CodeMirror === 'undefined') return;

  codeEditor = CodeMirror.fromTextArea(textarea, {
    mode: 'yaml',
    theme: 'dracula',
    lineNumbers: true,
    tabSize: 2,
    indentUnit: 2,
    autoCloseBrackets: true,
    lineWrapping: true,
    extraKeys: {
      'Tab': function(cm) {
        if (cm.somethingSelected()) {
          cm.indentSelection("add");
        } else {
          cm.replaceSelection("  ", "end");
        }
      },
      'Ctrl-S': function() { saveCurrentEditorFile(); },
      'Cmd-S': function() { saveCurrentEditorFile(); },
      'Ctrl-Enter': function() { runCurrentPlaybookInTerminal(); },
      'Cmd-Enter': function() { runCurrentPlaybookInTerminal(); }
    }
  });

  codeEditor.on('change', () => {
    if (!isEditorDirty) {
      isEditorDirty = true;
      if (editorSaveIndicator) {
        editorSaveIndicator.textContent = '● Unsaved';
        editorSaveIndicator.classList.add('unsaved');
      }
    }
  });

  if (btnEditorSave) {
    btnEditorSave.addEventListener('click', () => saveCurrentEditorFile());
  }
  if (btnEditorRun) {
    btnEditorRun.addEventListener('click', () => runCurrentPlaybookInTerminal());
  }

  // Execution flags (--check / --diff) toggles
  if (btnFlagCheck) {
    btnFlagCheck.addEventListener('click', (e) => {
      e.stopPropagation();
      activePlaybookFlags.check = !activePlaybookFlags.check;
      updateEditorRunButtonState();
      showFloatingToast(true, activePlaybookFlags.check ? '🔍 Check Mode active (--check)' : 'Check Mode off');
    });
  }
  if (btnFlagDiff) {
    btnFlagDiff.addEventListener('click', (e) => {
      e.stopPropagation();
      activePlaybookFlags.diff = !activePlaybookFlags.diff;
      updateEditorRunButtonState();
      showFloatingToast(true, activePlaybookFlags.diff ? '📄 Diff Mode active (--diff)' : 'Diff Mode off');
    });
  }

  // Dropdown menu trigger & options
  if (btnEditorRunDropdown && runOptionsMenu) {
    btnEditorRunDropdown.addEventListener('click', (e) => {
      e.stopPropagation();
      const isVisible = runOptionsMenu.style.display !== 'none';
      runOptionsMenu.style.display = isVisible ? 'none' : 'flex';
      btnEditorRunDropdown.setAttribute('aria-expanded', !isVisible);
    });

    document.addEventListener('click', () => {
      if (runOptionsMenu) {
        runOptionsMenu.style.display = 'none';
        if (btnEditorRunDropdown) btnEditorRunDropdown.setAttribute('aria-expanded', 'false');
      }
    });

    runOptionsMenu.querySelectorAll('.run-option-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.stopPropagation();
        runOptionsMenu.style.display = 'none';
        if (btnEditorRunDropdown) btnEditorRunDropdown.setAttribute('aria-expanded', 'false');
        const action = item.getAttribute('data-action');
        if (action === 'live') {
          activePlaybookFlags.check = false;
          activePlaybookFlags.diff = false;
          updateEditorRunButtonState();
          runCurrentPlaybookInTerminal();
        } else if (action === 'dry-run') {
          activePlaybookFlags.check = true;
          activePlaybookFlags.diff = true;
          updateEditorRunButtonState();
          runCurrentPlaybookInTerminal();
        } else if (action === 'check-only') {
          activePlaybookFlags.check = true;
          activePlaybookFlags.diff = false;
          updateEditorRunButtonState();
          runCurrentPlaybookInTerminal();
        } else if (action === 'diff-only') {
          activePlaybookFlags.check = false;
          activePlaybookFlags.diff = true;
          updateEditorRunButtonState();
          runCurrentPlaybookInTerminal();
        } else if (action === 'syntax-check') {
          runCurrentPlaybookSyntaxCheck();
        }
      });
    });
  }
  const btnEditorRevert = document.getElementById('btn-editor-revert');
  if (btnEditorRevert) {
    btnEditorRevert.addEventListener('click', () => {
      if (!confirm('Revert editor to clean starter template? Any unsaved edits will be discarded.')) return;
      const targetFile = currentExercise ? currentExercise.target_file : null;
      const fname = targetFile ? targetFile.replace(/^\/ansible\//, '') : (currentEditingPath || 'playbook.yml');
      revertEditorToCleanStarter(fname, currentExercise);
      showFloatingToast(true, 'Editor reverted to clean starter template.');
    });
  }

  setupSplitPaneResizer();
}

function revertEditorToCleanStarter(filename, exercise) {
  if (!codeEditor) return;
  const ex = exercise || currentExercise;
  const exTitle = ex ? (ex.title.split(':')[1]?.trim() || ex.title) : 'Playbook';
  const targetHosts = ex ? (ex.target || 'all') : 'all';
  const defaultContent = `---\n# ${filename} - ${exTitle}\n- name: ${exTitle}\n  hosts: ${targetHosts}\n  gather_facts: false\n  tasks:\n    \n`;
  codeEditor.setValue(defaultContent);
  if (codeEditor.clearHistory) {
    codeEditor.clearHistory();
  }
  isEditorDirty = false;
  currentEditingPath = filename;
  const nameEl = document.getElementById('editor-active-filename');
  if (nameEl) nameEl.textContent = filename;
  if (editorSaveIndicator) {
    editorSaveIndicator.textContent = '● Reset (Clean Template)';
    editorSaveIndicator.classList.remove('unsaved');
  }
  const ext = filename ? filename.split('.').pop().toLowerCase() : 'yml';
  if (ext === 'yml' || ext === 'yaml') {
    codeEditor.setOption('mode', 'yaml');
  } else if (ext === 'sh') {
    codeEditor.setOption('mode', 'shell');
  } else {
    codeEditor.setOption('mode', 'text');
  }
  setTimeout(() => {
    if (codeEditor) codeEditor.refresh();
  }, 50);
}

async function loadTargetLessonFile(filename) {
  if (!filename) return;
  currentEditingPath = filename;

  const nameEl = document.getElementById('editor-active-filename');
  if (nameEl) nameEl.textContent = filename;

  if (!codeEditor) return;

  try {
    const res = await fetch(`/api/files/content?path=${encodeURIComponent(filename)}`);
    if (res.ok) {
      const data = await res.json();
      if (data.content !== undefined) {
        codeEditor.setValue(data.content);
        isEditorDirty = false;
        if (editorSaveIndicator) {
          editorSaveIndicator.textContent = '✓ Synced';
          editorSaveIndicator.classList.remove('unsaved');
        }
      }
    } else {
      // File does not exist yet (clean state before user creates it)
      const exTitle = currentExercise ? (currentExercise.title.split(':')[1]?.trim() || currentExercise.title) : 'Playbook';
      const defaultContent = `---\n# ${filename} - ${exTitle}\n- name: ${exTitle}\n  hosts: ${currentExercise ? currentExercise.target || 'all' : 'all'}\n  gather_facts: false\n  tasks:\n    \n`;
      codeEditor.setValue(defaultContent);
      isEditorDirty = false;
      if (editorSaveIndicator) {
        editorSaveIndicator.textContent = '● New file (Unsaved)';
        editorSaveIndicator.classList.add('unsaved');
      }
    }

    const ext = filename.split('.').pop().toLowerCase();
    if (ext === 'yml' || ext === 'yaml') {
      codeEditor.setOption('mode', 'yaml');
    } else if (ext === 'sh') {
      codeEditor.setOption('mode', 'shell');
    } else {
      codeEditor.setOption('mode', 'text');
    }

    setTimeout(() => {
      if (codeEditor) codeEditor.refresh();
    }, 50);

  } catch (e) {
    console.error('Failed to load target file:', e);
  }
}

async function saveCurrentEditorFile() {
  if (!codeEditor || !currentEditingPath) return;
  const content = codeEditor.getValue();
  try {
    const res = await fetch('/api/files/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: currentEditingPath, content })
    });
    const data = await res.json();
    if (data.success) {
      isEditorDirty = false;
      if (editorSaveIndicator) {
        editorSaveIndicator.textContent = '✓ Saved';
        editorSaveIndicator.classList.remove('unsaved');
      }
    }
  } catch (e) {
    console.error('Failed to save file:', e);
  }
}

let activePlaybookFlags = {
  check: false,
  diff: false
};

function updateEditorRunButtonState() {
  if (btnFlagCheck) {
    btnFlagCheck.classList.toggle('active', activePlaybookFlags.check);
  }
  if (btnFlagDiff) {
    btnFlagDiff.classList.toggle('active', activePlaybookFlags.diff);
  }
  if (!btnEditorRunText) return;

  if (activePlaybookFlags.check && activePlaybookFlags.diff) {
    btnEditorRunText.textContent = 'Dry-Run (--check --diff)';
    if (btnEditorRunIcon) btnEditorRunIcon.textContent = '🔍';
  } else if (activePlaybookFlags.check) {
    btnEditorRunText.textContent = 'Check Mode (--check)';
    if (btnEditorRunIcon) btnEditorRunIcon.textContent = '🔍';
  } else if (activePlaybookFlags.diff) {
    btnEditorRunText.textContent = 'Diff Mode (--diff)';
    if (btnEditorRunIcon) btnEditorRunIcon.textContent = '📄';
  } else {
    btnEditorRunText.textContent = 'Run Playbook';
    if (btnEditorRunIcon) btnEditorRunIcon.textContent = '▶';
  }
}

async function runCurrentPlaybookInTerminal() {
  if (isEditorDirty) {
    await saveCurrentEditorFile();
  }
  if (!currentEditingPath) return;

  // If in Editor-only view, toggle to Split view so terminal is visible
  if (activeTab === 'editor') {
    switchTab('split');
  }

  const ext = currentEditingPath.split('.').pop().toLowerCase();
  let cmd = '';
  if (ext === 'yml' || ext === 'yaml') {
    let flags = [];
    if (activePlaybookFlags.check) flags.push('--check');
    if (activePlaybookFlags.diff) flags.push('--diff');
    const flagStr = flags.length > 0 ? ' ' + flags.join(' ') : '';
    cmd = `ansible-playbook ${currentEditingPath}${flagStr}\n`;
  } else if (ext === 'sh') {
    cmd = `bash ${currentEditingPath}\n`;
  } else {
    cmd = `cat ${currentEditingPath}\n`;
  }

  sendStringToTerminal(cmd);
}

async function runCurrentPlaybookSyntaxCheck() {
  if (isEditorDirty) {
    await saveCurrentEditorFile();
  }
  if (!currentEditingPath) return;
  if (activeTab === 'editor') {
    switchTab('split');
  }
  sendStringToTerminal(`ansible-playbook ${currentEditingPath} --syntax-check\n`);
}

// Split Pane Resizer between Editor & Terminal in Split View
function setupSplitPaneResizer() {
  if (!splitPaneResizer) return;
  let isDragging = false;
  let startY = 0;
  let startEditorH = 0;

  splitPaneResizer.addEventListener('mousedown', (e) => {
    isDragging = true;
    startY = e.clientY;
    startEditorH = viewEditor.getBoundingClientRect().height;
    document.body.style.cursor = 'row-resize';
    document.body.style.userSelect = 'none';
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const dy = e.clientY - startY;
    const newH = Math.max(120, startEditorH + dy);
    viewEditor.style.flex = `0 0 ${newH}px`;
    if (codeEditor) codeEditor.refresh();
    if (fitAddon) fitAddon.fit();
  });

  window.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      if (codeEditor) codeEditor.refresh();
      if (fitAddon) {
        fitAddon.fit();
        sendTerminalResize();
      }
    }
  });

  splitPaneResizer.addEventListener('dblclick', () => {
    viewEditor.style.flex = '1 1 50%';
    viewTerminal.style.flex = '1 1 50%';
    if (codeEditor) codeEditor.refresh();
    if (fitAddon) {
      fitAddon.fit();
      sendTerminalResize();
    }
  });
}

function showFloatingToast(isPass, msg, showNext = false) {
  if (!resultFloatingToast) return;
  if (toastIcon) {
    toastIcon.textContent = isPass ? '✓' : '✗';
    toastIcon.className = `toast-icon ${isPass ? 'pass' : 'fail'}`;
  }
  if (toastMsg) {
    toastMsg.textContent = msg;
  }
  if (btnToastNextLesson) {
    btnToastNextLesson.style.display = (isPass && showNext) ? 'inline-block' : 'none';
  }
  resultFloatingToast.style.display = 'flex';
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    hideFloatingToast();
  }, 9000);
}

function hideFloatingToast() {
  if (resultFloatingToast) {
    resultFloatingToast.style.display = 'none';
  }
}

// Next Lesson Navigation
function getNextExercise() {
  if (!curriculum || !curriculum.exercises || !currentExercise) return null;
  const currentIndex = curriculum.exercises.findIndex(e => e.id === currentExercise.id);
  if (currentIndex >= 0 && currentIndex < curriculum.exercises.length - 1) {
    return curriculum.exercises[currentIndex + 1];
  }
  return null;
}

function advanceToNextLesson() {
  const nextEx = getNextExercise();
  if (nextEx) {
    selectExercise(nextEx.id);
    switchTab('terminal');
    hideFloatingToast();
    if (term) term.focus();
  }
}

function setupNextLessonButtons() {
  if (btnToastNextLesson) {
    btnToastNextLesson.addEventListener('click', advanceToNextLesson);
  }
  if (btnNextExercise) {
    btnNextExercise.addEventListener('click', advanceToNextLesson);
  }
  if (btnNextLessonResults) {
    btnNextLessonResults.addEventListener('click', advanceToNextLesson);
  }
}

// Draggable Workspace Resizer
function setupWorkspaceResizer() {
  if (!workspaceResizer || !instructionPanel || !workspaceGrid) return;

  let isDragging = false;

  workspaceResizer.addEventListener('mousedown', () => {
    isDragging = true;
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const gridRect = workspaceGrid.getBoundingClientRect();
    const newWidth = e.clientX - gridRect.left;
    const totalWidth = gridRect.width;
    
    if (newWidth > 320 && newWidth < totalWidth * 0.75) {
      const pct = (newWidth / totalWidth) * 100;
      instructionPanel.style.width = `${pct}%`;
      if (fitAddon) {
        fitAddon.fit();
        sendTerminalResize();
      }
    }
  });

  window.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      if (fitAddon) {
        fitAddon.fit();
        sendTerminalResize();
      }
    }
  });

  workspaceResizer.addEventListener('dblclick', () => {
    instructionPanel.style.width = '48%';
    instructionPanel.style.display = 'flex';
    if (maxTermIcon) maxTermIcon.textContent = '⛶';
    setTimeout(() => {
      if (fitAddon) {
        fitAddon.fit();
        sendTerminalResize();
      }
    }, 50);
  });

  if (btnMaximizeTerm) {
    btnMaximizeTerm.addEventListener('click', () => {
      const isMax = instructionPanel.style.display === 'none';
      if (isMax) {
        instructionPanel.style.display = 'flex';
        workspaceResizer.style.display = 'block';
        if (maxTermIcon) maxTermIcon.textContent = '⛶';
      } else {
        instructionPanel.style.display = 'none';
        workspaceResizer.style.display = 'none';
        if (maxTermIcon) maxTermIcon.textContent = '🗗';
      }
      setTimeout(() => {
        if (fitAddon) {
          fitAddon.fit();
          sendTerminalResize();
        }
      }, 50);
    });
  }
}

// Global Keyboard Shortcuts
function setupKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      if (btnValidate) btnValidate.click();
      return;
    }

    if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'r' || e.key === 'R')) {
      e.preventDefault();
      if (btnReset) btnReset.click();
      return;
    }

    if (e.altKey && (e.key === 'i' || e.key === 'I')) {
      e.preventDefault();
      if (btnPeekNode) btnPeekNode.click();
      return;
    }

    if (e.altKey && (e.key === 'n' || e.key === 'N')) {
      e.preventDefault();
      advanceToNextLesson();
      return;
    }

    if (e.altKey && (e.key === 't' || e.key === 'T')) {
      e.preventDefault();
      const btnToggle = document.getElementById('btn-toggle-topology');
      if (btnToggle) btnToggle.click();
      return;
    }

    if (e.altKey && (e.key === 'm' || e.key === 'M')) {
      e.preventDefault();
      setLearningMode(currentLearningMode === 'guided' ? 'challenge' : 'guided');
      return;
    }

    if ((e.ctrlKey || e.metaKey) && e.key === 'ArrowRight') {
      e.preventDefault();
      setLessonStep('challenge');
      return;
    }

    if ((e.ctrlKey || e.metaKey) && e.key === 'ArrowLeft') {
      e.preventDefault();
      setLessonStep('primer');
      return;
    }

    if (e.key === 'Escape') {
      if (modalSettings && modalSettings.classList.contains('open')) {
        modalSettings.classList.remove('open');
      } else {
        hideFloatingToast();
      }
    }
  });
}

// Live Fleet Topology Toggle
function setupFleetTopologyToggle() {
  const btnToggle = document.getElementById('btn-toggle-topology');
  const btnClose = document.getElementById('btn-close-hud');
  const fleetHud = document.getElementById('fleet-hud');
  if (!btnToggle || !fleetHud) return;

  // Defaults to FALSE (hidden) so terminal gets maximum screen real estate
  const isVisible = localStorage.getItem('fleet_topology_visible') === 'true';
  setTopologyVisible(isVisible);

  function setTopologyVisible(show) {
    fleetHud.style.display = show ? 'block' : 'none';
    btnToggle.classList.toggle('active', show);
    btnToggle.setAttribute('aria-expanded', show ? 'true' : 'false');
    localStorage.setItem('fleet_topology_visible', show ? 'true' : 'false');
    if (fitAddon) {
      setTimeout(() => {
        try {
          fitAddon.fit();
          sendTerminalResize();
        } catch (e) {}
      }, 50);
    }
  }

  btnToggle.addEventListener('click', () => {
    const willShow = fleetHud.style.display === 'none';
    setTopologyVisible(willShow);
  });

  if (btnClose) {
    btnClose.addEventListener('click', () => {
      setTopologyVisible(false);
    });
  }
}

// Two-Stage Learning Architecture (Concept Primer vs Mission Challenge)
function setLessonStep(step) {
  currentLessonStep = step;
  if (btnStepPrimer) btnStepPrimer.classList.toggle('active', step === 'primer');
  if (btnStepChallenge) btnStepChallenge.classList.toggle('active', step === 'challenge');

  if (stepPanePrimer) stepPanePrimer.style.display = (step === 'primer') ? 'block' : 'none';
  if (stepPaneChallenge) stepPaneChallenge.style.display = (step === 'challenge') ? 'block' : 'none';

  if (step === 'challenge') {
    if (currentExercise && currentExercise.target_file) {
      if (activeTab === 'terminal') switchTab('split');
    }
    // Start MTTR / Speedrun timer when entering challenge
    if (!scenarioStartTime && currentExercise) {
      startScenarioTimer(currentExercise);
    }
  }
}

function setLearningMode(mode) {
  currentLearningMode = mode;
  localStorage.setItem('ansible_learning_mode', mode);

  if (modeGuided) {
    modeGuided.classList.toggle('active', mode === 'guided');
    modeGuided.setAttribute('aria-checked', mode === 'guided' ? 'true' : 'false');
  }
  if (modeChallenge) {
    modeChallenge.classList.toggle('active', mode === 'challenge');
    modeChallenge.setAttribute('aria-checked', mode === 'challenge' ? 'true' : 'false');
  }

  if (mode === 'challenge') {
    setLessonStep('challenge');
  } else {
    setLessonStep('primer');
  }
  updateLessonXpDisplay();
}

function setupLearningModeSwitcher() {
  if (modeGuided) {
    modeGuided.addEventListener('click', () => {
      setLearningMode('guided');
      showFloatingToast(true, '🎓 Guided Learning Mode: Concept & Syntax first, zero XP deduction!');
    });
  }
  if (modeChallenge) {
    modeChallenge.addEventListener('click', () => {
      setLearningMode('challenge');
      showFloatingToast(true, '⚡ Challenge-Only Mode: +25% Hardcore Bonus XP on no-hint completions!');
    });
  }
  setLearningMode(currentLearningMode);
}

function setupLessonStepNav() {
  if (btnStepPrimer) {
    btnStepPrimer.addEventListener('click', () => setLessonStep('primer'));
  }
  if (btnStepChallenge) {
    btnStepChallenge.addEventListener('click', () => setLessonStep('challenge'));
  }
  if (btnAdvanceChallenge) {
    btnAdvanceChallenge.addEventListener('click', () => {
      setLessonStep('challenge');
      showFloatingToast(true, '⏱️ Mission challenge started! MTTR timer active.');
    });
  }
  if (btnBackToPrimer) {
    btnBackToPrimer.addEventListener('click', () => setLessonStep('primer'));
  }

  if (btnCopyBlueprint) {
    btnCopyBlueprint.addEventListener('click', () => {
      const codeEl = document.querySelector('#primer-code-view code');
      if (codeEl && codeEl.textContent) {
        navigator.clipboard.writeText(codeEl.textContent);
        showFloatingToast(true, 'Syntax blueprint copied to clipboard!');
      }
    });
  }

  if (btnInsertBlueprint) {
    btnInsertBlueprint.addEventListener('click', () => {
      const codeEl = document.querySelector('#primer-code-view code');
      const snippet = codeEl ? codeEl.textContent : '';
      if (!snippet) return;

      if (currentExercise && currentExercise.target_file && codeEditor) {
        codeEditor.setValue(snippet);
        switchTab('editor');
        showFloatingToast(true, 'Loaded blueprint skeleton into editor. Customize it for your mission!');
      } else {
        switchTab('terminal');
        sendStringToTerminal(snippet);
        showFloatingToast(true, 'Pasted syntax skeleton into terminal (edit to match your mission)!');
      }
    });
  }
}

function renderPrimer(ex) {
  const conceptBody = document.getElementById('primer-concept-body');
  const codeView = document.getElementById('primer-code-view');
  const breakdownList = document.getElementById('primer-syntax-breakdown');
  const tipCard = document.getElementById('primer-tip-card');
  const tipBody = document.getElementById('primer-tip-body');
  const btnInsertLabel = document.getElementById('btn-insert-blueprint-label');

  if (!conceptBody || !codeView) return;

  // 1. Concept: from ex.primer.concept or extract from explanation
  let conceptText = '';
  if (ex.primer && ex.primer.concept) {
    conceptText = ex.primer.concept;
  } else if (ex.explanation) {
    const parts = ex.explanation.split(/```/);
    conceptText = parts[0] || ex.explanation;
  } else {
    conceptText = "Learn the essential concepts and syntax before executing commands on the live cluster.";
  }
  conceptBody.innerHTML = renderSimpleMarkdown(conceptText);

  // 2. Companion Sample Files (External vars, templates)
  const companionContainer = document.getElementById('primer-companion-files');
  const mainFileHeader = document.getElementById('primer-main-file-header');
  const mainFilePath = document.getElementById('primer-main-file-path');
  const mainFileBadge = document.getElementById('primer-main-file-badge');

  if (companionContainer) {
    if (ex.primer && Array.isArray(ex.primer.sample_files) && ex.primer.sample_files.length > 0) {
      companionContainer.innerHTML = ex.primer.sample_files.map((file) => `
        <div class="primer-companion-card">
          <div class="primer-file-header">
            <div class="primer-file-title-wrap">
              <span class="primer-file-badge companion-badge">${escapeHtml(file.badge || '📄 Sample File')}</span>
              <span class="primer-file-path">${escapeHtml(file.path || '')}</span>
            </div>
            <button class="btn btn-secondary btn-xs btn-copy-companion" data-code="${escapeHtml(file.code || '')}" title="Copy file content">📋 Copy</button>
          </div>
          ${file.desc ? `<div class="primer-file-desc">${escapeHtml(file.desc)}</div>` : ''}
          <pre class="code-block primer-code-block companion-code-block"><code>${escapeHtml(file.code || '')}</code></pre>
        </div>
      `).join('');
      companionContainer.style.display = 'flex';

      companionContainer.querySelectorAll('.btn-copy-companion').forEach(btn => {
        btn.addEventListener('click', () => {
          const code = btn.getAttribute('data-code');
          if (code) {
            navigator.clipboard.writeText(code);
            showFloatingToast(true, 'Sample file copied to clipboard!');
          }
        });
      });

      if (mainFileHeader) {
        if (mainFileBadge) {
          mainFileBadge.textContent = ex.target_file ? '📘 Playbook' : '💻 Command Blueprint';
        }
        if (mainFilePath) {
          mainFilePath.textContent = ex.target_file || '';
        }
        mainFileHeader.style.display = 'flex';
      }
    } else {
      companionContainer.innerHTML = '';
      companionContainer.style.display = 'none';
      if (mainFileHeader) mainFileHeader.style.display = 'none';
    }
  }

  // 3. Demo Code: from ex.primer.demo_code or ex.solution_code
  const demoCode = (ex.primer && ex.primer.demo_code) ? ex.primer.demo_code : (ex.solution_code || '');
  codeView.querySelector('code').textContent = demoCode;

  // Update insert label
  if (btnInsertLabel) {
    btnInsertLabel.textContent = ex.target_file ? '📝 Load Template Skeleton' : '💻 Paste Syntax to Terminal';
  }

  // 3. Syntax Breakdown
  if (breakdownList) {
    if (ex.primer && Array.isArray(ex.primer.syntax_breakdown) && ex.primer.syntax_breakdown.length > 0) {
      breakdownList.innerHTML = ex.primer.syntax_breakdown.map(item => `
        <div class="syntax-item">
          <span class="syntax-element">${escapeHtml(item.element)}</span>
          <span class="syntax-role">${escapeHtml(item.role)}</span>
        </div>
      `).join('');
      breakdownList.style.display = 'flex';
    } else {
      breakdownList.innerHTML = '';
      breakdownList.style.display = 'none';
    }
  }

  // 4. Pro-Tip
  if (tipCard && tipBody) {
    const tipText = (ex.primer && ex.primer.quick_tip) ? ex.primer.quick_tip : '';
    if (tipText) {
      tipBody.innerHTML = renderSimpleMarkdown(tipText);
      tipCard.style.display = 'flex';
    } else {
      tipCard.style.display = 'none';
    }
  }
}

// Load Curriculum
async function loadCurriculum() {
  try {
    const res = await fetch('/api/curriculum');
    curriculum = await res.json();
    renderCurriculumNav();
    if (curriculum.exercises && curriculum.exercises.length > 0) {
      selectExercise(curriculum.exercises[0].id);
    }
  } catch (err) {
    curriculumList.innerHTML = `<div class="p-4" style="color:var(--rose-danger);padding:14px;">Error loading curriculum: ${escapeHtml(err.message)}</div>`;
  }
}

function renderCurriculumNav() {
  curriculumList.innerHTML = '';
  if (!curriculum || !curriculum.modules) return;

  curriculum.modules.forEach(mod => {
    const group = document.createElement('div');
    group.className = 'module-group';
    
    const modExercises = curriculum.exercises.filter(e => e.module === mod.id);
    const modSolved = modExercises.filter(e => localStorage.getItem(`validated_${e.id}`) === 'true').length;

    const title = document.createElement('div');
    title.className = 'module-group-title';
    title.style.display = 'flex';
    title.style.justifyContent = 'space-between';
    title.style.alignItems = 'center';
    title.innerHTML = `<span>${escapeHtml(mod.title)}</span> <span style="font-size:10.5px;color:var(--primary-indigo);font-weight:600;">${modSolved}/${modExercises.length}</span>`;
    group.appendChild(title);

    modExercises.forEach((ex, idx) => {
      const item = document.createElement('div');
      item.className = 'nav-item';
      item.id = `nav-${ex.id}`;
      item.onclick = () => selectExercise(ex.id);

      const isDone = localStorage.getItem(`validated_${ex.id}`) === 'true';
      const isBoss = ex.title.includes('MINI-BOSS');
      if (isBoss) {
        item.classList.add('nav-item-boss');
      }

      const leftWrap = document.createElement('div');
      leftWrap.className = 'nav-item-left';

      const numSpan = document.createElement('span');
      numSpan.className = 'nav-item-num';
      if (isBoss) {
        numSpan.style.color = 'var(--amber-warning)';
        numSpan.style.fontWeight = '700';
      }
      const cleanNum = ex.title.match(/Lesson\s+(\d+\.\d+)/i) ? ex.title.match(/Lesson\s+(\d+\.\d+)/i)[1] : (idx + 1);
      numSpan.textContent = cleanNum;

      const label = document.createElement('span');
      label.className = 'nav-item-title';
      let cleanTitle = ex.title.includes(':') ? ex.title.split(':')[1].trim() : ex.title;
      if (isBoss) {
        label.innerHTML = `<span style="color:var(--amber-warning);font-weight:700;">🚨 BOSS:</span> ${escapeHtml(cleanTitle.replace(/^MINI-BOSS:\s*/i, '').replace(/^CAPSTONE MINI-BOSS:\s*/i, ''))}`;
      } else {
        label.textContent = cleanTitle;
      }

      leftWrap.appendChild(numSpan);
      leftWrap.appendChild(label);

      const rightWrap = document.createElement('div');
      rightWrap.className = 'nav-item-right';

      if (isDone) {
        const check = document.createElement('span');
        check.className = 'nav-check-done';
        check.textContent = '✓';
        check.title = 'Completed';
        rightWrap.appendChild(check);
      }

      const xpBadge = document.createElement('span');
      xpBadge.className = 'nav-xp-badge';
      if (isDone) {
        const earned = localStorage.getItem(`earned_xp_${ex.id}`);
        xpBadge.textContent = `+${earned ? earned : (ex.xp || 50)} XP`;
      } else {
        xpBadge.textContent = `+${ex.xp || 50} XP`;
      }
      rightWrap.appendChild(xpBadge);

      item.appendChild(leftWrap);
      item.appendChild(rightWrap);
      group.appendChild(item);
    });

    curriculumList.appendChild(group);
  });
}

function selectExercise(exId) {
  const ex = curriculum.exercises.find(e => e.id === exId);
  if (!ex) return;
  currentExercise = ex;

  // Scoped file & editor enablement check
  const targetFile = ex.target_file;
  if (targetFile) {
    if (tabBtnEditor) {
      tabBtnEditor.disabled = false;
      tabBtnEditor.classList.remove('tab-disabled');
      tabBtnEditor.title = 'In-Browser Playbook Editor Full View';
    }
    if (tabBtnSplit) {
      tabBtnSplit.disabled = false;
      tabBtnSplit.classList.remove('tab-disabled');
      tabBtnSplit.title = 'Dual Workspace (Editor + Terminal)';
    }

    const cleanFilename = targetFile.replace(/^\/ansible\//, '');
    loadTargetLessonFile(cleanFilename);

    if (activeTab !== 'editor') {
      switchTab('split');
    }
  } else {
    // Ad-hoc lesson: Editor not needed, disable it completely!
    if (tabBtnEditor) {
      tabBtnEditor.disabled = true;
      tabBtnEditor.classList.add('tab-disabled');
      tabBtnEditor.title = 'Ad-hoc CLI Mission — Playbook Editor disabled for this lesson';
    }
    if (tabBtnSplit) {
      tabBtnSplit.disabled = true;
      tabBtnSplit.classList.add('tab-disabled');
      tabBtnSplit.title = 'Ad-hoc CLI Mission — Playbook Editor disabled for this lesson';
    }

    currentEditingPath = '';
    const nameEl = document.getElementById('editor-active-filename');
    if (nameEl) nameEl.textContent = 'None (Ad-hoc Mission)';

    switchTab('terminal');
  }
  clearTerminalShell();
  resetScenarioTimerStandby(ex);

  // Context-aware execution flag presets
  if (ex.id === 'l2-13-dry-run-check' || (ex.tasks && ex.tasks.some(t => t.includes('--check')))) {
    activePlaybookFlags.check = true;
    activePlaybookFlags.diff = true;
  } else {
    activePlaybookFlags.check = false;
    activePlaybookFlags.diff = false;
  }
  updateEditorRunButtonState();

  // Update active item in sidebar
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  const activeNav = document.getElementById(`nav-${ex.id}`);
  if (activeNav) activeNav.classList.add('active');

  // Breadcrumb & Title
  const mod = curriculum.modules.find(m => m.id === ex.module);
  if (exerciseBreadcrumb) {
    exerciseBreadcrumb.textContent = mod ? mod.title.split(':')[0] : 'Level 1';
  }
  if (exerciseTitlePill) {
    const pillText = ex.title.match(/Lesson\s+\d+\.\d+/i) ? ex.title.match(/Lesson\s+\d+\.\d+/i)[0] : ex.title.split(':')[0].trim();
    exerciseTitlePill.textContent = pillText;
  }
  if (exerciseTicket) {
    exerciseTicket.textContent = ex.ticket_id || `Mission ${ex.id.split('-')[0].toUpperCase()}`;
  }
  if (exerciseTitle) {
    exerciseTitle.textContent = ex.title;
  }

  // Target chip
  if (scenTargetChip) {
    scenTargetChip.textContent = `Target: ${ex.target || 'all'}`;
  }

  // Tags
  const diff = ex.difficulty || 'Beginner';
  const solType = (ex.solution_type || 'playbook').toUpperCase();
  if (exerciseTags) {
    exerciseTags.innerHTML = `
      <span class="nav-xp-badge" id="lesson-xp-badge" style="font-size:11px;padding:2px 8px;">⚡ +${ex.xp || 50} XP</span>
      <span class="nav-pill pill-${diff.toLowerCase()}">${diff}</span>
      <span class="tag">${solType}</span>
    `;
  }

  // Challenge briefing
  const scenarioText = ex.scenario || ex.objective;
  if (objectiveContent) {
    objectiveContent.innerHTML = renderSimpleMarkdown(scenarioText);
  }

  // Render Interactive Task Checklist
  renderChecklist(ex);

  // Render Concept Primer & set initial step based on Learning Mode
  renderPrimer(ex);
  if (currentLearningMode === 'challenge') {
    setLessonStep('challenge');
  } else {
    setLessonStep('primer');
  }

  // Guide
  if (guideContent) {
    guideContent.innerHTML = renderSimpleMarkdown(ex.explanation);
  }

  // Progressive Hints
  renderHints(ex);

  // Collapse non-essential sections by default
  if (accordionGuide) accordionGuide.open = false;
  if (accordionHints) accordionHints.open = false;
  if (accordionTargetState) accordionTargetState.open = false;

  // Reset Solution state
  if (solutionWrapper) solutionWrapper.style.display = 'none';
  if (solutionCodeView) {
    solutionCodeView.querySelector('code').textContent = ex.solution_code;
  }

  // Reset Node Peek box
  if (inspectCmdLabel) {
    inspectCmdLabel.textContent = `SSH: ${ex.inspect_cmd || 'uname -a'} [target: ${ex.target || 'all'}]`;
  }
  if (inspectOutput) {
    inspectOutput.textContent = `Target: [${ex.target}]\nCommand: ${ex.inspect_cmd || 'uname -a'}\n\nClick 'Run Node Inspect' (Alt+I) to query live target state.`;
  }

  // Update dynamic XP badge and penalty summaries
  updateLessonXpDisplay();

  // Reset validation tab status
  if (valBadgeChip) {
    valBadgeChip.className = 'tab-status-chip ready';
    valBadgeChip.textContent = 'Ready';
  }
  if (valDetails) {
    valDetails.innerHTML = `Run <strong>Check Solution</strong> to test your solution against the cluster.`;
  }
  if (terminalOutput) {
    terminalOutput.innerHTML = `<span class="terminal-placeholder">Ready to execute tests for ${escapeHtml(ex.title)}.</span>`;
  }
  // Update Next Lesson buttons visibility
  const nextEx = getNextExercise();
  const isCurrentDone = localStorage.getItem(`validated_${ex.id}`) === 'true';
  if (btnNextExercise) {
    btnNextExercise.style.display = (isCurrentDone && nextEx) ? 'inline-flex' : 'none';
    if (nextEx) btnNextExercise.title = `Advance to ${nextEx.title.split(':')[0]}`;
  }
  if (btnNextLessonResults) {
    btnNextLessonResults.style.display = (isCurrentDone && nextEx) ? 'inline-flex' : 'none';
  }
  if (btnToastNextLesson) {
    btnToastNextLesson.style.display = 'none';
  }

  // Provision scenario environment on target nodes
  provisionScenarioEnvironment(ex);
}

// Gamification XP Calculation & Penalty System
function getExercisePenaltyBreakdown(ex) {
  if (!ex) return { baseXp: 50, currentXp: 50, penalty: 0, hintPenalty: 10, solutionPenalty: 25, openedHints: [], isSolutionRevealed: false, minXp: 10, isHardcore: false };
  const baseXp = ex.xp || 50;
  const openedHints = JSON.parse(localStorage.getItem(`hints_opened_${ex.id}`) || '[]');
  const isSolutionRevealed = localStorage.getItem(`solution_revealed_${ex.id}`) === 'true';

  const hintPenalty = Math.max(5, Math.round(baseXp * 0.15));
  const solutionPenalty = Math.max(10, Math.round(baseXp * 0.40));

  let totalPenalty = 0;
  totalPenalty += (openedHints.length * hintPenalty);
  if (isSolutionRevealed) totalPenalty += solutionPenalty;

  const minXp = Math.max(10, Math.round(baseXp * 0.20));
  let calculatedXp = Math.max(minXp, baseXp - totalPenalty);

  // Hardcore Bonus: In Challenge Mode, if completed without hints or solution, +25% bonus XP!
  const isHardcore = (currentLearningMode === 'challenge' && totalPenalty === 0);
  if (isHardcore) {
    calculatedXp = Math.round(baseXp * 1.25);
  }

  return {
    baseXp,
    currentXp: calculatedXp,
    penalty: totalPenalty,
    hintPenalty,
    solutionPenalty,
    openedHints,
    isSolutionRevealed,
    minXp,
    isHardcore
  };
}

function calculateCurrentLessonXp(ex) {
  return getExercisePenaltyBreakdown(ex).currentXp;
}

function updateLessonXpDisplay(triggerNotice = false, noticeMsg = '') {
  if (!currentExercise) return;
  const info = getExercisePenaltyBreakdown(currentExercise);
  const isDone = localStorage.getItem(`validated_${currentExercise.id}`) === 'true';
  const savedEarned = localStorage.getItem(`earned_xp_${currentExercise.id}`);
  const earnedXp = savedEarned ? parseInt(savedEarned) : info.currentXp;

  // Header tag XP badge
  const xpBadge = document.getElementById('lesson-xp-badge');
  if (xpBadge) {
    if (isDone) {
      xpBadge.className = 'nav-xp-badge';
      xpBadge.textContent = `⚡ Solved (+${earnedXp} XP)`;
    } else if (info.isHardcore) {
      xpBadge.className = 'nav-xp-badge';
      xpBadge.textContent = `⚡ +${info.currentXp} XP (Hardcore +25%)`;
    } else if (info.penalty === 0) {
      xpBadge.className = 'nav-xp-badge';
      xpBadge.textContent = `⚡ +${info.baseXp} XP (Full Reward)`;
    } else {
      xpBadge.className = 'nav-xp-badge xp-reduced';
      xpBadge.textContent = `⚡ +${info.currentXp} XP (-${info.penalty} XP assistance)`;
    }
  }

  // Guide accordion badge
  if (guideXpBadge) {
    if (info.isGuideOpened) {
      guideXpBadge.className = 'summary-badge penalty-applied';
      guideXpBadge.textContent = `Applied (-${info.guidePenalty} XP)`;
    } else {
      guideXpBadge.className = 'summary-badge penalty-badge';
      guideXpBadge.textContent = `-${info.guidePenalty} XP if opened`;
    }
  }

  // Hints accordion badge
  if (hintsXpBadge) {
    if (info.openedHints.length > 0) {
      hintsXpBadge.className = 'summary-badge penalty-applied';
      hintsXpBadge.textContent = `Applied (-${info.openedHints.length * info.hintPenalty} XP)`;
    } else {
      hintsXpBadge.className = 'summary-badge penalty-badge';
      hintsXpBadge.textContent = `-${info.hintPenalty} XP per hint`;
    }
  }

  // Reveal Solution button text
  if (btnRevealSolution) {
    if (info.isSolutionRevealed) {
      btnRevealSolution.textContent = (solutionWrapper && solutionWrapper.style.display !== 'none') ? 'Hide Solution' : 'View Solution';
    } else {
      btnRevealSolution.textContent = `Reveal Solution (-${info.solutionPenalty} XP)`;
    }
  }

  if (triggerNotice && noticeMsg && activeTab === 'terminal') {
    showFloatingToast(false, noticeMsg);
  }
}

function renderChecklist(ex) {
  if (!tasksChecklist) return;
  tasksChecklist.innerHTML = '';
  const savedChecks = JSON.parse(localStorage.getItem(`checklist_${ex.id}`) || '[]');
  const tasks = ex.tasks || [];

  tasks.forEach((taskText, idx) => {
    const li = document.createElement('li');
    li.className = 'checklist-item';
    const isChecked = savedChecks.includes(idx);
    if (isChecked) li.classList.add('completed');

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = `chk-${ex.id}-${idx}`;
    checkbox.checked = isChecked;

    const label = document.createElement('label');
    label.htmlFor = checkbox.id;
    label.textContent = taskText;

    checkbox.addEventListener('change', () => {
      let currentSaved = JSON.parse(localStorage.getItem(`checklist_${ex.id}`) || '[]');
      if (checkbox.checked) {
        if (!currentSaved.includes(idx)) currentSaved.push(idx);
        li.classList.add('completed');
      } else {
        currentSaved = currentSaved.filter(i => i !== idx);
        li.classList.remove('completed');
      }
      localStorage.setItem(`checklist_${ex.id}`, JSON.stringify(currentSaved));
    });

    li.appendChild(checkbox);
    li.appendChild(label);
    tasksChecklist.appendChild(li);
  });
}

function renderHints(ex) {
  if (!hintsContainer) return;
  hintsContainer.innerHTML = '';
  const hints = ex.hints || [];

  if (hints.length === 0) {
    hintsContainer.innerHTML = '<div style="font-size:13px;color:var(--text-muted);padding:8px 0;">No extra hints needed for this scenario. Follow the Conceptual Guide above!</div>';
    return;
  }

  const info = getExercisePenaltyBreakdown(ex);
  const openedHints = info.openedHints;

  hints.forEach((hint, idx) => {
    const details = document.createElement('details');
    details.className = 'hint-step';
    const isAlreadyOpened = openedHints.includes(idx);
    if (isAlreadyOpened) details.open = true;

    const summary = document.createElement('summary');
    const badgeText = isAlreadyOpened ? ' (Used)' : ` (-${info.hintPenalty} XP)`;
    summary.innerHTML = `<span style="display:flex;justify-content:space-between;width:100%;align-items:center;"><span>💡 ${hint.level || `Hint ${idx + 1}`}</span><span style="font-size:11px;opacity:0.8;">${badgeText}</span></span>`;

    const content = document.createElement('div');
    content.className = 'hint-step-content';
    content.innerHTML = renderSimpleMarkdown(hint.body || hint.text || '');

    details.addEventListener('toggle', () => {
      if (details.open && currentExercise && currentExercise.id === ex.id) {
        const curInfo = getExercisePenaltyBreakdown(currentExercise);
        const curOpened = curInfo.openedHints;
        if (!curOpened.includes(idx)) {
          curOpened.push(idx);
          localStorage.setItem(`hints_opened_${currentExercise.id}`, JSON.stringify(curOpened));
          const newInfo = getExercisePenaltyBreakdown(currentExercise);
          updateLessonXpDisplay(true, `💡 Hint ${idx + 1} opened: Potential reward is now +${newInfo.currentXp} XP (-${curInfo.hintPenalty} XP)`);
        }
      }
    });

    details.appendChild(summary);
    details.appendChild(content);
    hintsContainer.appendChild(details);
  });
}

let currentSetupId = 0;

async function provisionScenarioEnvironment(ex) {
  const setupId = ++currentSetupId;
  if (!ex.setup_playbook && !ex.reset_playbook) return;

  try {
    const res = await fetch(`/api/exercise/${ex.id}/setup`, { method: 'POST' });
    const data = await res.json();
    if (setupId === currentSetupId && currentExercise && currentExercise.id === ex.id) {
      fetchNodeInspect(ex);
    }
  } catch (err) {
    // Non-blocking background setup
  }
}

async function fetchNodeInspect(ex) {
  if (!inspectOutput || !ex) return;
  inspectOutput.textContent = `⏳ Querying ${ex.target} nodes over SSH: '${ex.inspect_cmd || 'uname -a'}'...`;
  try {
    const res = await fetch(`/api/exercise/${ex.id}/inspect`, { method: 'POST' });
    const data = await res.json();
    inspectOutput.textContent = `$ ${data.command} [target: ${data.target}]\n\n${data.output}`;
  } catch (err) {
    inspectOutput.textContent = `Node inspection failed: ${err.message}`;
  }
}

function setupScenarioFeatures() {
  if (btnPeekNode) {
    btnPeekNode.addEventListener('click', () => {
      if (currentExercise) fetchNodeInspect(currentExercise);
    });
  }

  if (accordionGuide) {
    accordionGuide.addEventListener('toggle', () => {
      if (accordionGuide.open && currentExercise) {
        if (localStorage.getItem(`guide_opened_${currentExercise.id}`) !== 'true') {
          localStorage.setItem(`guide_opened_${currentExercise.id}`, 'true');
          const newInfo = getExercisePenaltyBreakdown(currentExercise);
          updateLessonXpDisplay(true, `📖 Guide opened: Potential reward is now +${newInfo.currentXp} XP (-${newInfo.guidePenalty} XP)`);
        }
      }
    });
  }

  if (btnRevealSolution) {
    btnRevealSolution.addEventListener('click', () => {
      if (!solutionWrapper || !currentExercise) return;
      const isHidden = solutionWrapper.style.display === 'none' || solutionWrapper.style.display === '';
      solutionWrapper.style.display = isHidden ? 'block' : 'none';

      if (isHidden && localStorage.getItem(`solution_revealed_${currentExercise.id}`) !== 'true') {
        localStorage.setItem(`solution_revealed_${currentExercise.id}`, 'true');
        const newInfo = getExercisePenaltyBreakdown(currentExercise);
        updateLessonXpDisplay(true, `⚠️ Solution revealed: Potential reward is now +${newInfo.currentXp} XP (-${newInfo.solutionPenalty} XP)`);
      }
      btnRevealSolution.textContent = isHidden ? 'Hide Solution' : (localStorage.getItem(`solution_revealed_${currentExercise.id}`) === 'true' ? 'View Solution' : `Reveal Solution`);
    });
  }

  if (btnCopySolution) {
    btnCopySolution.addEventListener('click', async () => {
      if (!currentExercise) return;
      try {
        await navigator.clipboard.writeText(currentExercise.solution_code);
        const prev = btnCopySolution.textContent;
        btnCopySolution.textContent = '✅ Copied!';
        setTimeout(() => { btnCopySolution.textContent = prev; }, 1800);
      } catch (err) {
        const ta = document.createElement('textarea');
        ta.value = currentExercise.solution_code;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        btnCopySolution.textContent = '✅ Copied!';
        setTimeout(() => { btnCopySolution.textContent = '📋 Copy Command'; }, 1800);
      }
    });
  }

  if (btnPasteTerminal) {
    btnPasteTerminal.addEventListener('click', () => {
      if (!currentExercise) return;
      const code = currentExercise.solution_code;
      if (currentExercise.solution_type === 'command') {
        sendStringToTerminal(code + '\n');
      } else {
        sendStringToTerminal(`cat << 'EOF' > /tmp/solution.yml\n${code}\nEOF\nansible-playbook /tmp/solution.yml\n`);
      }
      switchTab('terminal');
      if (term) term.focus();
    });
  }
}

// Execution Actions
function setupExecutionActions() {
  if (btnValidate) {
    btnValidate.addEventListener('click', async () => {
      if (!currentExercise) return;
      if (currentLessonStep === 'primer') {
        setLessonStep('challenge');
      }
      setTerminalStatus('running', 'Validating...');
      if (valBadgeChip) {
        valBadgeChip.className = 'tab-status-chip';
        valBadgeChip.textContent = 'RUNNING';
      }
      if (valDetails) {
        valDetails.textContent = 'Running automated assertion tests against live cluster nodes...';
      }
      if (terminalOutput) {
        terminalOutput.textContent = `Validating assertions for ${currentExercise.title}...\n`;
      }

      try {
        const res = await fetch(`/api/exercise/${currentExercise.id}/validate`, {
          method: 'POST'
        });
        const data = await res.json();
        if (terminalOutput) {
          terminalOutput.textContent = data.output;
        }

        // Synchronize interactive checklist with task results
        if (data.tasks_results && Array.isArray(data.tasks_results) && tasksChecklist) {
          const items = tasksChecklist.querySelectorAll('.checklist-item');
          data.tasks_results.forEach((tr, i) => {
            if (items[i]) {
              const chk = items[i].querySelector('input[type="checkbox"]');
              if (tr.status === 'passed') {
                items[i].classList.add('completed');
                items[i].classList.remove('has-error');
                if (chk) chk.checked = true;
              } else if (tr.status === 'failed') {
                items[i].classList.remove('completed');
                items[i].classList.add('has-error');
                if (chk) chk.checked = false;
              }
            }
          });
        }

        if (data.passed) {
          if (valBadgeChip) {
            valBadgeChip.className = 'tab-status-chip pass';
            valBadgeChip.textContent = 'PASS';
          }
          setTerminalStatus('online', 'Passed');

          // Speedrun timer & MTTR metrics
          const elapsedSeconds = stopScenarioTimer();
          const mttrFormatted = formatTime(elapsedSeconds);
          const isIncident = currentExercise.id.endsWith('-10') || (currentExercise.tags || []).some(t => t.toLowerCase().includes('incident'));
          let speedrunBonus = 0;
          if (isIncident) {
            if (elapsedSeconds <= 180) speedrunBonus = 50;
            else if (elapsedSeconds <= 300) speedrunBonus = 25;
          }

          // Streak & Combo multiplier
          const info = getExercisePenaltyBreakdown(currentExercise);
          const isFlawless = (info.penalty === 0);
          let currentStreak = parseInt(localStorage.getItem('ansible_streak') || '0');
          if (isFlawless) currentStreak += 1;
          localStorage.setItem('ansible_streak', currentStreak);

          const highestStreak = parseInt(localStorage.getItem('ansible_highest_streak') || '0');
          if (currentStreak > highestStreak) {
            localStorage.setItem('ansible_highest_streak', currentStreak);
          }

          let comboMultiplier = 1.0;
          if (currentStreak >= 5) comboMultiplier = 2.0;
          else if (currentStreak >= 3) comboMultiplier = 1.5;
          else if (currentStreak >= 2) comboMultiplier = 1.25;

          const baseAwarded = calculateCurrentLessonXp(currentExercise);
          const totalAwarded = Math.round(baseAwarded * comboMultiplier) + speedrunBonus;
          localStorage.setItem(`earned_xp_${currentExercise.id}`, totalAwarded);

          // Save validated state
          localStorage.setItem(`validated_${currentExercise.id}`, 'true');

          if (valDetails) {
            let msg = `All target state assertions passed in ${data.duration}s! (Elapsed: ${mttrFormatted})`;
            if (isIncident && speedrunBonus > 0) {
              msg += ` ⚡ Speedrun Bonus: +${speedrunBonus} XP!`;
            }
            if (comboMultiplier > 1.0) {
              msg += ` 🔥 Combo: ${comboMultiplier}x multiplier active!`;
            }
            valDetails.textContent = msg;
          }

          // Procedural Audio Feedback
          const nextEx = getNextExercise();
          if (!nextEx) {
            playFanfare();
          } else if (comboMultiplier > 1.0) {
            playSparkleChime();
          } else {
            playPassChime();
          }

          // Trigger XP pulse animation
          if (hudXpPill) {
            hudXpPill.classList.remove('pulse');
            void hudXpPill.offsetWidth;
            hudXpPill.classList.add('pulse');
          }

          // Trigger celebration confetti
          triggerCelebrationConfetti();

          // Check Badges & Achievements
          checkAndAwardBadges({
            isIncident,
            elapsedSeconds,
            idempotencyPassed: data.output && data.output.includes('Idempotency verified')
          });

          renderCurriculumNav();
          updateProgressTracker();
          updateLessonXpDisplay();
          const activeNav = document.getElementById(`nav-${currentExercise.id}`);
          if (activeNav) activeNav.classList.add('active');

          if (nextEx) {
            if (btnNextExercise) {
              btnNextExercise.style.display = 'inline-flex';
              btnNextExercise.title = `Next: ${nextEx.title.split(':')[0]}`;
            }
            if (btnNextLessonResults) {
              btnNextLessonResults.style.display = 'inline-flex';
            }
          }

          if (activeTab === 'terminal') {
            const isFull = (info.penalty === 0);
            const comboTag = comboMultiplier > 1.0 ? ` (${comboMultiplier}x Combo! 🔥)` : '';
            const bonusTag = speedrunBonus > 0 ? ` (+${speedrunBonus} Speedrun XP)` : '';
            showFloatingToast(true, `Passed in ${data.duration}s! +${totalAwarded} XP${comboTag}${bonusTag} ${isFull ? '(Flawless! 🌟)' : '(Assisted)'} (MTTR: ${mttrFormatted})`, !!nextEx);
          }
        } else {
          // Play Failure Audio Tone
          playFailAlert();

          // Reset streak on failed test
          localStorage.setItem('ansible_streak', 0);
          updateProgressTracker();

          if (valBadgeChip) {
            valBadgeChip.className = 'tab-status-chip fail';
            valBadgeChip.textContent = 'FAIL';
          }
          const failCount = (data.tasks_results || []).filter(t => t.status === 'failed').length;
          const totalCount = (data.tasks_results || []).length;
          if (valDetails) {
            valDetails.textContent = failCount > 0 
              ? `${failCount} of ${totalCount} scenario tasks failed criteria. Review task diagnostics below.`
              : `Target state did not match expected criteria. Review assertions below.`;
          }
          setTerminalStatus('failed', 'Failed');

          if (activeTab === 'terminal') {
            showFloatingToast(false, failCount > 0 ? `Validation: ${failCount} task(s) failed — View results` : 'Validation failed — View log');
          }
        }
      } catch (err) {
        if (terminalOutput) {
          terminalOutput.textContent = `Validation check failed: ${err.message}`;
        }
        setTerminalStatus('offline', 'Error');
        if (valBadgeChip) {
          valBadgeChip.className = 'tab-status-chip fail';
          valBadgeChip.textContent = 'ERROR';
        }
      }
    });
  }

  if (btnReset) {
    btnReset.addEventListener('click', async () => {
      if (!currentExercise) return;
      if (!confirm(`Reset and restore targets for "${currentExercise.title}" to clean baseline?`)) return;

      // Always reset validation, earned XP, and penalties on reset
      localStorage.removeItem(`validated_${currentExercise.id}`);
      localStorage.removeItem(`earned_xp_${currentExercise.id}`);
      localStorage.removeItem(`guide_opened_${currentExercise.id}`);
      localStorage.removeItem(`hints_opened_${currentExercise.id}`);
      localStorage.removeItem(`solution_revealed_${currentExercise.id}`);

      // Hide Next Lesson buttons
      if (btnNextExercise) btnNextExercise.style.display = 'none';
      if (btnNextLessonResults) btnNextLessonResults.style.display = 'none';

      // Collapse accordions
      if (accordionGuide) accordionGuide.open = false;
      if (accordionHints) accordionHints.open = false;
      if (accordionTargetState) accordionTargetState.open = false;

      // Update sidebar nav, progress tracker, and XP display
      renderCurriculumNav();
      updateProgressTracker();
      updateLessonXpDisplay();
      resetScenarioTimerStandby(currentExercise);
      renderPrimer(currentExercise);
      if (currentLearningMode === 'challenge') {
        setLessonStep('challenge');
      } else {
        setLessonStep('primer');
      }
      clearTerminalShell();

      setTerminalStatus('running', 'Resetting...');
      if (valBadgeChip) {
        valBadgeChip.className = 'tab-status-chip';
        valBadgeChip.textContent = 'RESETTING';
      }
      if (valDetails) {
        valDetails.textContent = `Executing reset & target re-provisioning...`;
      }
      if (terminalOutput) {
        terminalOutput.textContent = `Resetting cluster state...\n`;
      }

      try {
        const res = await fetch(`/api/exercise/${currentExercise.id}/reset`, {
          method: 'POST'
        });
        const data = await res.json();
        if (terminalOutput) {
          terminalOutput.textContent = data.output || "Reset completed successfully.";
        }
        setTerminalStatus('online', 'Reset Done');
        if (valBadgeChip) {
          valBadgeChip.className = 'tab-status-chip ready';
          valBadgeChip.textContent = 'Ready';
        }
        if (valDetails) {
          valDetails.textContent = 'Reset completed. Nodes prepared for scenario.';
        }

        // Reset terminal PTY session to guarantee fresh shell with ECHO enabled
        if (termSocket && termSocket.readyState === WebSocket.OPEN) {
          termSocket.send(JSON.stringify({ type: 'reset' }));
          if (term) {
            term.clear();
            term.focus();
          }
        }

        // Guaranteed revert of editor to clean starter template
        if (currentExercise && currentExercise.target_file) {
          const cleanFilename = currentExercise.target_file.replace(/^\/ansible\//, '');
          revertEditorToCleanStarter(cleanFilename, currentExercise);
        } else if (currentEditingPath) {
          revertEditorToCleanStarter(currentEditingPath, currentExercise);
        }

        if (currentExercise) {
          provisionScenarioEnvironment(currentExercise);
        }
        showFloatingToast(true, 'Lab, terminal shell & playbook file reset to pristine baseline!');
      } catch (err) {
        if (terminalOutput) {
          terminalOutput.textContent = `Reset failed: ${err.message}`;
        }
        setTerminalStatus('offline', 'Error');
      }
    });
  }
}

// Progress & Gamification Tracker
function updateProgressTracker() {
  if (!curriculum || !curriculum.exercises) return;
  const total = curriculum.exercises.length || 40;
  const solved = curriculum.exercises.filter(e => localStorage.getItem(`validated_${e.id}`) === 'true').length;
  
  if (userProgressText) userProgressText.textContent = `${solved}/${total} Completed`;
  if (userProgressBar) {
    const pct = Math.round((solved / total) * 100);
    userProgressBar.style.width = `${pct}%`;
  }
  if (userProgressAria) userProgressAria.setAttribute('aria-valuenow', solved);

  // Total XP
  let totalXp = 0;
  curriculum.exercises.forEach(e => {
    if (localStorage.getItem(`validated_${e.id}`) === 'true') {
      const earned = localStorage.getItem(`earned_xp_${e.id}`);
      totalXp += earned ? parseInt(earned) : (e.xp || 50);
    }
  });

  if (hudXpAmount) hudXpAmount.textContent = `${totalXp} XP`;

  // Streak & Combo Multiplier
  const streak = parseInt(localStorage.getItem('ansible_streak') || '0');
  let comboMult = 1.0;
  if (streak >= 5) comboMult = 2.0;
  else if (streak >= 3) comboMult = 1.5;
  else if (streak >= 2) comboMult = 1.25;

  if (hudStreakCount) {
    hudStreakCount.textContent = comboMult > 1.0 ? `${streak} (${comboMult}x 🔥)` : `${streak}`;
  }

  const streakPill = document.getElementById('hud-streak-pill');
  if (streakPill) {
    if (comboMult > 1.0) {
      streakPill.classList.add('combo-active');
      streakPill.title = `${streak} Flawless Solves! Active Combo: ${comboMult}x XP Multiplier`;
    } else {
      streakPill.classList.remove('combo-active');
      streakPill.title = 'Consecutive Solved Streak';
    }
  }

  updateBadgesHUD();

  // Rank determination
  let rankIcon = '🔰';
  let rankName = 'Novice Sysadmin';
  if (solved >= 40) {
    rankIcon = '🏆';
    rankName = 'DataForge Hero';
  } else if (solved >= 30) {
    rankIcon = '🔮';
    rankName = 'Senior Architect';
  } else if (solved >= 20) {
    rankIcon = '🛡️';
    rankName = 'Infra Specialist';
  } else if (solved >= 10) {
    rankIcon = '🚀';
    rankName = 'Fleet Operator';
  } else if (solved >= 4) {
    rankIcon = '🛠️';
    rankName = 'Junior Automation';
  }

  if (hudRankIcon) hudRankIcon.textContent = rankIcon;
  if (hudRankName) hudRankName.textContent = rankName;
}

// Fullscreen Confetti Particle Celebration Engine
function triggerCelebrationConfetti() {
  const canvas = document.getElementById('confetti-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particles = [];
  const colors = ['#6366f1', '#10b981', '#f59e0b', '#ec4899', '#38bdf8', '#a855f7', '#fbbf24'];

  for (let i = 0; i < 75; i++) {
    particles.push({
      x: window.innerWidth * (0.35 + Math.random() * 0.3),
      y: window.innerHeight * 0.65,
      vx: (Math.random() - 0.5) * 15,
      vy: -(Math.random() * 14 + 7),
      size: Math.random() * 8 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * 360,
      vRot: (Math.random() - 0.5) * 12,
      opacity: 1
    });
  }

  let startTime = null;
  function animate(time) {
    if (!startTime) startTime = time;
    const elapsed = time - startTime;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.38;
      p.rotation += p.vRot;
      p.opacity = Math.max(0, 1 - elapsed / 2600);

      ctx.save();
      ctx.globalAlpha = p.opacity;
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.5);
      ctx.restore();
    });

    if (elapsed < 2600) {
      requestAnimationFrame(animate);
    } else {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  }

  requestAnimationFrame(animate);
}

function setTerminalStatus(state, text) {
  if (!terminalStatus) return;
  const dotClass = state === 'online' ? 'dot-online' : 'dot-offline';
  terminalStatus.innerHTML = `<span class="status-dot ${dotClass}"></span> ${escapeHtml(text)}`;
}

// ==========================================================
// PROCEDURAL WEB AUDIO FX ENGINE
// ==========================================================
let audioCtx = null;
let isAudioMuted = localStorage.getItem('ansible_lab_audio_muted') === 'true';

function getAudioContext() {
  try {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        audioCtx = new AudioContextClass();
      }
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  } catch (e) {
    // Graceful fallback for non-supported browsers
  }
  return audioCtx;
}

function initAudioSynthesizer() {
  const btnToggleSound = document.getElementById('btn-toggle-sound');
  const soundIcon = document.getElementById('sound-icon');

  function updateSoundButton() {
    if (soundIcon) soundIcon.textContent = isAudioMuted ? '🔇' : '🔊';
    if (btnToggleSound) {
      btnToggleSound.title = isAudioMuted ? 'Unmute Audio FX (Currently Muted)' : 'Mute Audio FX (Currently Enabled)';
    }
  }

  if (btnToggleSound) {
    btnToggleSound.addEventListener('click', () => {
      isAudioMuted = !isAudioMuted;
      localStorage.setItem('ansible_lab_audio_muted', isAudioMuted);
      updateSoundButton();
      if (!isAudioMuted) {
        playSparkleChime();
      }
    });
  }
  updateSoundButton();
}

function playPassChime() {
  if (isAudioMuted) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
  notes.forEach((freq, idx) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.08);

    gain.gain.setValueAtTime(0, ctx.currentTime + idx * 0.08);
    gain.gain.linearRampToValueAtTime(0.18, ctx.currentTime + idx * 0.08 + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.08 + 0.35);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(ctx.currentTime + idx * 0.08);
    osc.stop(ctx.currentTime + idx * 0.08 + 0.38);
  });
}

function playFailAlert() {
  if (isAudioMuted) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'triangle';
  osc.frequency.setValueAtTime(220, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(130, ctx.currentTime + 0.3);

  gain.gain.setValueAtTime(0.2, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.32);

  osc.connect(gain);
  gain.connect(ctx.destination);

  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + 0.35);
}

function playSparkleChime() {
  if (isAudioMuted) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const freqs = [880, 1318.5, 1760];
  freqs.forEach((freq, idx) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.06);

    gain.gain.setValueAtTime(0.12, ctx.currentTime + idx * 0.06);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.06 + 0.25);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(ctx.currentTime + idx * 0.06);
    osc.stop(ctx.currentTime + idx * 0.06 + 0.28);
  });
}

function playBossAlert() {
  if (isAudioMuted) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  [0, 0.2].forEach(delay => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(440, ctx.currentTime + delay);
    osc.frequency.exponentialRampToValueAtTime(220, ctx.currentTime + delay + 0.15);

    gain.gain.setValueAtTime(0.15, ctx.currentTime + delay);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + delay + 0.16);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(ctx.currentTime + delay);
    osc.stop(ctx.currentTime + delay + 0.18);
  });
}

function playFanfare() {
  if (isAudioMuted) return;
  const ctx = getAudioContext();
  if (!ctx) return;

  const notes = [523.25, 659.25, 783.99, 1046.50, 1318.51];
  notes.forEach((freq, idx) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.1);

    gain.gain.setValueAtTime(0.16, ctx.currentTime + idx * 0.1);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.1 + 0.5);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(ctx.currentTime + idx * 0.1);
    osc.stop(ctx.currentTime + idx * 0.1 + 0.55);
  });
}

// ==========================================================
// SPEEDRUN TIMERS & MTTR INCIDENT SCORING
// ==========================================================
let scenarioStartTime = null;
let incidentTimerInterval = null;

function formatTime(seconds) {
  if (!seconds || seconds < 0) return '00:00';
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function resetScenarioTimerStandby(ex) {
  if (incidentTimerInterval) {
    clearInterval(incidentTimerInterval);
    incidentTimerInterval = null;
  }
  scenarioStartTime = null;
  if (hudTimerVal) hudTimerVal.textContent = '00:00';
  if (hudTimerPill) {
    hudTimerPill.style.display = 'inline-flex';
    hudTimerPill.classList.remove('incident-timer');
    hudTimerPill.classList.add('standby');
    hudTimerPill.title = 'Standby — MTTR timer starts when entering challenge';
  }
}

function startScenarioTimer(ex) {
  if (incidentTimerInterval) {
    clearInterval(incidentTimerInterval);
    incidentTimerInterval = null;
  }

  scenarioStartTime = Date.now();
  if (hudTimerVal) hudTimerVal.textContent = '00:00';

  const isIncident = ex && (ex.id.endsWith('-10') || (ex.tags || []).some(t => t.toLowerCase().includes('incident')));
  if (hudTimerPill) {
    hudTimerPill.style.display = 'inline-flex';
    hudTimerPill.classList.remove('standby');
    if (isIncident) {
      hudTimerPill.classList.add('incident-timer');
      hudTimerPill.title = 'Active Incident Remediation Timer (MTTR Speedrun)';
      playBossAlert();
    } else {
      hudTimerPill.classList.remove('incident-timer');
      hudTimerPill.title = 'Scenario Elapsed Time';
    }
  }

  incidentTimerInterval = setInterval(() => {
    if (!scenarioStartTime) return;
    const elapsedSec = Math.floor((Date.now() - scenarioStartTime) / 1000);
    if (hudTimerVal) hudTimerVal.textContent = formatTime(elapsedSec);
  }, 1000);
}

function stopScenarioTimer() {
  if (incidentTimerInterval) {
    clearInterval(incidentTimerInterval);
    incidentTimerInterval = null;
  }
  if (!scenarioStartTime) return 0;
  const elapsed = Math.floor((Date.now() - scenarioStartTime) / 1000);
  scenarioStartTime = null;
  return elapsed;
}

// ==========================================================
// SRE ACHIEVEMENTS & BADGES SHELF
// ==========================================================
const SRE_BADGES = [
  { id: 'first_contact', icon: '🔰', title: 'First Contact', desc: 'Successfully complete Lesson 1.1 on the cluster', xpReward: 50 },
  { id: 'adhoc_commander', icon: '⚡', title: 'Ad-Hoc Commander', desc: 'Complete all 10 Level 1 ad-hoc missions', xpReward: 150 },
  { id: 'playbook_architect', icon: '📝', title: 'Playbook Architect', desc: 'Author and execute your first YAML playbook (Lesson 2.1)', xpReward: 75 },
  { id: 'zero_drift', icon: '🔒', title: 'Zero Drift Master', desc: 'Pass a playbook with Phase 3 automated idempotency verified', xpReward: 100 },
  { id: 'ghost_hunter', icon: '👻', title: 'Ghost Hunter', desc: 'Remediate Incident #1042: Phantom Port Conflict (Mini-Boss 1)', xpReward: 200 },
  { id: 'canary_rescuer', icon: '🐤', title: 'Canary Rescuer', desc: 'Remediate Incident #2089: Split-Brain Production Outage (Mini-Boss 2)', xpReward: 200 },
  { id: 'speed_demon', icon: '⏱️', title: 'Speed Demon', desc: 'Remediate any SRE incident with MTTR under 3 minutes', xpReward: 125 },
  { id: 'combo_master', icon: '🔥', title: 'Flawless Combo x3', desc: 'Solve 3 consecutive scenarios without using hints or reveals', xpReward: 150 },
  { id: 'fleet_champion', icon: '👑', title: 'Fleet Champion', desc: 'Complete all 40 lessons across the entire SRE curriculum', xpReward: 500 }
];

function getUnlockedBadges() {
  return JSON.parse(localStorage.getItem('ansible_unlocked_badges') || '{}');
}

function saveUnlockedBadge(badgeId) {
  const badges = getUnlockedBadges();
  if (!badges[badgeId]) {
    badges[badgeId] = new Date().toISOString();
    localStorage.setItem('ansible_unlocked_badges', JSON.stringify(badges));
    return true;
  }
  return false;
}

function checkAndAwardBadges(context = {}) {
  const currentUnlocked = getUnlockedBadges();
  const newlyUnlocked = [];

  SRE_BADGES.forEach(badge => {
    if (currentUnlocked[badge.id]) return;

    let unlocked = false;
    if (badge.id === 'first_contact') {
      if (localStorage.getItem('validated_l1-1-first-contact') === 'true' || localStorage.getItem('validated_l1-1') === 'true') unlocked = true;
    } else if (badge.id === 'adhoc_commander') {
      const l1Exercises = curriculum?.exercises?.filter(e => e.module === 'lvl1') || [];
      const l1Solved = l1Exercises.length > 0 && l1Exercises.every(e => localStorage.getItem(`validated_${e.id}`) === 'true');
      if (l1Solved) unlocked = true;
    } else if (badge.id === 'playbook_architect') {
      if (localStorage.getItem('validated_l2-1-first-playbook') === 'true' || localStorage.getItem('validated_l2-1') === 'true') unlocked = true;
    } else if (badge.id === 'zero_drift') {
      if (context.idempotencyPassed) unlocked = true;
    } else if (badge.id === 'ghost_hunter') {
      if (localStorage.getItem('validated_l1-11-fleet-cleanup') === 'true' || localStorage.getItem('validated_l1-10-fleet-cleanup') === 'true') unlocked = true;
    } else if (badge.id === 'canary_rescuer') {
      if (localStorage.getItem('validated_l2-13-dry-run-check') === 'true' || localStorage.getItem('validated_l2-10-dry-run-check') === 'true') unlocked = true;
    } else if (badge.id === 'speed_demon') {
      if (context.isIncident && context.elapsedSeconds && context.elapsedSeconds <= 180) unlocked = true;
    } else if (badge.id === 'combo_master') {
      const streak = parseInt(localStorage.getItem('ansible_streak') || '0');
      if (streak >= 3) unlocked = true;
    } else if (badge.id === 'fleet_champion') {
      if (curriculum && curriculum.exercises) {
        const allDone = curriculum.exercises.every(e => localStorage.getItem(`validated_${e.id}`) === 'true');
        if (allDone) unlocked = true;
      }
    }

    if (unlocked) {
      if (saveUnlockedBadge(badge.id)) {
        newlyUnlocked.push(badge);
      }
    }
  });

  if (newlyUnlocked.length > 0) {
    const first = newlyUnlocked[0];
    playSparkleChime();
    triggerCelebrationConfetti();
    showFloatingToast(true, `🏆 Achievement Unlocked: ${first.title}! (+${first.xpReward} Bonus XP)`);
  }

  updateBadgesHUD();
}

function updateBadgesHUD() {
  const unlocked = getUnlockedBadges();
  const count = Object.keys(unlocked).length;
  if (hudBadgeCount) {
    hudBadgeCount.textContent = `${count}/${SRE_BADGES.length} Badges`;
  }
}

function renderBadgesShelf() {
  const grid = document.getElementById('badges-grid');
  const unlocked = getUnlockedBadges();
  const unlockedCount = Object.keys(unlocked).length;

  const countEl = document.getElementById('badges-unlocked-count');
  if (countEl) countEl.textContent = `${unlockedCount} / ${SRE_BADGES.length}`;

  let totalBonusXp = 0;
  SRE_BADGES.forEach(b => {
    if (unlocked[b.id]) totalBonusXp += b.xpReward;
  });
  const bonusXpEl = document.getElementById('badges-total-bonus-xp');
  if (bonusXpEl) bonusXpEl.textContent = `+${totalBonusXp} XP`;

  const highestStreak = localStorage.getItem('ansible_highest_streak') || localStorage.getItem('ansible_streak') || '0';
  const streakEl = document.getElementById('badges-highest-streak');
  if (streakEl) streakEl.textContent = `${highestStreak} 🔥`;

  if (!grid) return;
  grid.innerHTML = '';

  SRE_BADGES.forEach(badge => {
    const isUnlocked = !!unlocked[badge.id];
    const card = document.createElement('div');
    card.className = `badge-card ${isUnlocked ? 'unlocked' : 'locked'}`;

    const dateStr = isUnlocked ? new Date(unlocked[badge.id]).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : 'Locked';

    card.innerHTML = `
      <div class="badge-card-header">
        <div class="badge-icon-wrap">${isUnlocked ? badge.icon : '🔒'}</div>
        <div class="badge-card-titles">
          <span class="badge-title-text">${badge.title}</span>
          <span class="badge-xp-reward">+${badge.xpReward} Bonus XP</span>
        </div>
      </div>
      <div class="badge-desc-text">${badge.desc}</div>
      <div class="badge-footer-meta">
        <span class="badge-date-meta">${isUnlocked ? `Unlocked: ${dateStr}` : 'Incomplete'}</span>
        <span class="badge-status-pill ${isUnlocked ? 'unlocked' : 'locked'}">${isUnlocked ? '✓ EARNED' : 'LOCKED'}</span>
      </div>
    `;
    grid.appendChild(card);
  });
}

function setupBadgesModal() {
  const btnCloseBadges = document.getElementById('btn-close-badges');
  const modalBadges = document.getElementById('modal-badges');

  if (btnOpenBadges && modalBadges) {
    btnOpenBadges.addEventListener('click', () => {
      renderBadgesShelf();
      modalBadges.classList.add('active');
    });
  }

  if (btnCloseBadges && modalBadges) {
    btnCloseBadges.addEventListener('click', () => {
      modalBadges.classList.remove('active');
    });
  }

  if (modalBadges) {
    modalBadges.addEventListener('click', (e) => {
      if (e.target === modalBadges) {
        modalBadges.classList.remove('active');
      }
    });
  }

  updateBadgesHUD();
}

// ==========================================================
// EXPORT LAB REPO PORTFOLIO GENERATOR
// ==========================================================
function setupRepoExport() {
  const btnExport = document.getElementById('btn-export-repo');
  if (!btnExport) return;

  btnExport.addEventListener('click', () => {
    showFloatingToast(true, '📦 Bundling Ansible portfolio ZIP...');
    playSparkleChime();
    window.location.href = '/api/workspace/export';
  });
}

// Cluster Fleet Modal & Full Rollback
function setupSettingsModal() {
  if (btnOpenSettings && modalSettings) {
    btnOpenSettings.addEventListener('click', () => {
      modalSettings.classList.add('open');
      refreshClusterMetrics();
    });
  }

  if (btnCloseSettings && modalSettings) {
    btnCloseSettings.addEventListener('click', () => {
      modalSettings.classList.remove('open');
    });
  }

  if (modalSettings) {
    modalSettings.addEventListener('click', (e) => {
      if (e.target === modalSettings) modalSettings.classList.remove('open');
    });
  }

  if (btnFullRollback) {
    btnFullRollback.addEventListener('click', async () => {
      if (!confirm("Are you sure you want to rollback ALL 6 NODES to the baseline? This restores pristine state across the entire cluster.")) {
        return;
      }

      if (rollbackStatus) rollbackStatus.textContent = "Initiating container reset across all 6 nodes...\n";
      btnFullRollback.disabled = true;

      try {
        const res = await fetch('/api/cluster/rollback', { method: 'POST' });
        const data = await res.json();
        if (rollbackStatus) {
          rollbackStatus.textContent = (data.log || "Done") + "\n\nAll nodes restored to clean baseline!";
        }
        await refreshClusterMetrics();
      } catch (err) {
        if (rollbackStatus) rollbackStatus.textContent = "Rollback failed: " + err.message;
      } finally {
        btnFullRollback.disabled = false;
      }
    });
  }
}

async function refreshClusterMetrics() {
  if (!clusterTableBody) return;
  try {
    const res = await fetch('/api/cluster/status');
    const data = await res.json();
    renderClusterTable(data.nodes);
  } catch (err) {
    clusterTableBody.innerHTML = `<tr><td colspan="6" style="color:var(--rose-danger);padding:12px;">Error querying cluster: ${escapeHtml(err.message)}</td></tr>`;
  }
}

function renderClusterTable(nodes) {
  if (!clusterTableBody || !nodes) return;
  clusterTableBody.innerHTML = '';
  nodes.forEach(n => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${escapeHtml(n.name)}</strong></td>
      <td>${escapeHtml(n.os)}</td>
      <td><span class="status-dot ${n.status === 'running' ? 'dot-online' : 'dot-offline'}"></span> ${escapeHtml(n.status)}</td>
      <td><span style="color:${n.ping === 'OK' ? '#10b981' : '#f43f5e'};font-weight:600;">${escapeHtml(n.ping)}</span></td>
      <td>${escapeHtml(n.ram_used_mb)} / ${escapeHtml(n.ram_total_mb)} MB</td>
      <td>${escapeHtml(n.disk_used_gb)} / ${escapeHtml(n.disk_total_gb)} GB</td>
    `;
    clusterTableBody.appendChild(tr);
  });
}

let fleetEventSource = null;

function initFleetTelemetryStream() {
  if (!!window.EventSource) {
    if (fleetEventSource) {
      fleetEventSource.close();
    }
    fleetEventSource = new EventSource('/api/cluster/telemetry/stream');

    fleetEventSource.onmessage = (event) => {
      try {
        const nodes = JSON.parse(event.data);
        if (Array.isArray(nodes) && nodes.length > 0) {
          updateFleetHUD(nodes);
        }
      } catch (e) {
        console.error('Failed to parse telemetry stream:', e);
      }
    };

    fleetEventSource.onerror = (e) => {
      const sseBadge = document.getElementById('fleet-sse-badge');
      if (sseBadge) {
        sseBadge.textContent = '⚠ Reconnecting...';
        sseBadge.classList.add('offline');
      }
      pollClusterStatus();
    };

    fleetEventSource.onopen = () => {
      const sseBadge = document.getElementById('fleet-sse-badge');
      if (sseBadge) {
        sseBadge.textContent = '⚡ Live SSE';
        sseBadge.classList.remove('offline');
      }
    };
  } else {
    pollClusterStatus();
    setInterval(pollClusterStatus, 4000);
  }
}

function updateFleetHUD(nodes) {
  const onlineCount = nodes.filter(n => n.status === 'running' || n.ping === 'OK').length;
  
  // Header pill update
  const dot = document.getElementById('global-cluster-dot');
  const txt = document.getElementById('global-cluster-status');
  if (txt) txt.textContent = `${onlineCount}/${nodes.length} Nodes Online`;
  if (dot) dot.className = `status-dot ${onlineCount === nodes.length ? 'dot-online' : 'dot-offline'}`;

  // Fleet HUD summary update
  const summary = document.getElementById('fleet-hud-summary');
  if (summary) {
    summary.textContent = `${onlineCount}/${nodes.length} Nodes Online • Telemetry Active`;
  }

  const grid = document.getElementById('fleet-microgrid');
  if (!grid) return;

  // Render cards if empty or node count changed
  if (grid.children.length !== nodes.length) {
    grid.innerHTML = nodes.map(n => {
      const isOnline = n.status === 'running' || n.ping === 'OK';
      const badgeClass = `badge-${(n.badge || n.family || 'distro').toLowerCase()}`;
      const changedClass = n.is_changed ? 'pulse-changed' : '';
      const pingText = n.latency_ms ? `${n.latency_ms}ms` : (n.ping === 'OK' ? 'OK' : 'FAIL');
      const ramText = n.ram_used_mb ? `${n.ram_used_mb}MB` : '12MB';

      return `
        <div class="fleet-node-card ${isOnline ? 'status-online' : 'status-offline'} ${changedClass}" 
             id="fnc-${n.name}" 
             data-name="${n.name}"
             title="${n.name} (${n.os}) - Click to Ping in Terminal">
          <div class="fnc-header">
            <span class="fnc-badge ${badgeClass}">${escapeHtml(n.badge || 'NODE')}</span>
            <span class="fnc-dot"></span>
          </div>
          <div class="fnc-name">${escapeHtml(n.name)}</div>
          <div class="fnc-metrics">
            <span class="fnc-metric fnc-ping" id="fnc-ping-${n.name}">⚡ ${escapeHtml(pingText)}</span>
            <span class="fnc-metric fnc-mem" id="fnc-mem-${n.name}">🧠 ${escapeHtml(ramText)}</span>
          </div>
        </div>
      `;
    }).join('');

    // Attach click listeners to cards to send ping command to terminal
    nodes.forEach(n => {
      const card = document.getElementById(`fnc-${n.name}`);
      if (card) {
        card.addEventListener('click', () => {
          const tabBtn = document.getElementById('tab-btn-terminal');
          if (tabBtn) tabBtn.click();
          sendStringToTerminal(`ansible ${n.name} -m ping\n`);
        });
      }
    });
  } else {
    // In-place updates to avoid DOM re-creation
    nodes.forEach(n => {
      const card = document.getElementById(`fnc-${n.name}`);
      if (card) {
        const isOnline = n.status === 'running' || n.ping === 'OK';
        card.className = `fleet-node-card ${isOnline ? 'status-online' : 'status-offline'} ${n.is_changed ? 'pulse-changed' : ''}`;
        
        const pingEl = document.getElementById(`fnc-ping-${n.name}`);
        if (pingEl) {
          const pingText = n.latency_ms ? `${n.latency_ms}ms` : (n.ping === 'OK' ? 'OK' : 'FAIL');
          pingEl.textContent = `⚡ ${pingText}`;
        }

        const memEl = document.getElementById(`fnc-mem-${n.name}`);
        if (memEl && n.ram_used_mb) {
          memEl.textContent = `🧠 ${n.ram_used_mb}MB`;
        }
      }
    });
  }
}

async function pollClusterStatus() {
  try {
    const res = await fetch('/api/cluster/status');
    const data = await res.json();
    const onlineCount = data.nodes.filter(n => n.ping === 'OK').length;
    const dot = document.getElementById('global-cluster-dot');
    const txt = document.getElementById('global-cluster-status');
    if (txt) txt.textContent = `${onlineCount}/${data.nodes.length} Nodes Online`;
    if (dot) dot.className = `status-dot ${onlineCount === data.nodes.length ? 'dot-online' : 'dot-offline'}`;
  } catch (e) {}
}

// Helpers
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderSimpleMarkdown(md) {
  if (!md) return '';
  let html = md
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/```([a-z]*)\n([\s\S]*?)```/gim, '<pre class="code-block"><code>$2</code></pre>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
    .replace(/^\* (.*$)/gim, '<li>$1</li>')
    .replace(/^(\d+)\.\s+(.*$)/gim, '<li>$2</li>')
    .replace(/\n\n/gim, '</p><p>');
  return `<p>${html}</p>`;
}
