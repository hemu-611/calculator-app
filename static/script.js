const displayExpr   = document.getElementById('display-expr');
const displayResult = document.getElementById('display-result');
const historyList   = document.getElementById('history-list');
const btnClearHist  = document.getElementById('btn-clear-history');

let expr = '';

// ── Expression helpers ────────────────────────────────────────────────────────

function setExpr(value) {
  expr = value;
  displayExpr.textContent = expr || ' ';
}

function insert(text) {
  expr += text;
  displayExpr.textContent = expr;
}

function backspace() {
  expr = expr.slice(0, -1);
  displayExpr.textContent = expr || ' ';
  if (!expr) setResult('0', false);
}

function clearAll() {
  setExpr('');
  setResult('0', false);
}

function setResult(text, isError) {
  displayResult.textContent = text;
  displayResult.classList.toggle('error', isError);
}

// ── API calls ─────────────────────────────────────────────────────────────────

async function evaluate() {
  if (!expr.trim()) return;

  try {
    const res  = await fetch('/calculate', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ expr }),
    });
    const data = await res.json();

    if (data.error) {
      setResult(data.error, true);
    } else {
      setResult(data.result, false);
      setExpr(data.result);
      addHistoryItem(expr, data.result);
    }
  } catch {
    setResult('Network error', true);
  }
}

async function clearHistory() {
  await fetch('/history', { method: 'DELETE' });
  historyList.innerHTML = '<li class="history-empty">No calculations yet</li>';
}

// ── History UI ────────────────────────────────────────────────────────────────

function addHistoryItem(expression, result) {
  const empty = historyList.querySelector('.history-empty');
  if (empty) empty.remove();

  const li = document.createElement('li');
  li.className = 'history-item';
  li.innerHTML = `
    <div class="history-item-expr">${escHtml(expression)}</div>
    <div class="history-item-result">${escHtml(result)}</div>
  `;
  li.addEventListener('click', () => {
    setExpr(result);
    setResult(result, false);
  });

  historyList.prepend(li);
}

function escHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ── Button clicks ─────────────────────────────────────────────────────────────

document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const action = btn.dataset.action;
    const value  = btn.dataset.insert;

    if (action === 'clear')    return clearAll();
    if (action === 'backspace') return backspace();
    if (action === 'evaluate') return evaluate();
    if (value !== undefined)   return insert(value);
  });
});

btnClearHist.addEventListener('click', clearHistory);

// ── Keyboard support ──────────────────────────────────────────────────────────

document.addEventListener('keydown', e => {
  if (e.ctrlKey || e.altKey || e.metaKey) return;

  if (e.key === 'Enter' || e.key === '=') { e.preventDefault(); return evaluate(); }
  if (e.key === 'Backspace')               { e.preventDefault(); return backspace(); }
  if (e.key === 'Escape')                  { e.preventDefault(); return clearAll(); }

  const allowed = /^[0-9+\-*/.%^(),a-z_ ]$/i;
  if (allowed.test(e.key)) insert(e.key);
});
