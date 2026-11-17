import { blockElements } from './message-view.js';
let hintKey = '', recordKey = '';
export function renderPanels(game, busy) {
  const key = game.id + game.hints.map(h => h.id).join();
  if (key !== hintKey) {
    const panel = document.querySelector('#hints'); panel.replaceChildren();
    if (!game.hints.length) { const p = document.createElement('p'); p.className = 'muted'; p.textContent = 'Ninguna todavía. Pueden avanzar con sus propias ideas.'; panel.append(p); }
    game.hints.forEach(hint => { const article = document.createElement('article'); const label = document.createElement('strong'); label.textContent = hint.id.startsWith('B') ? 'Apoyo de binario' : 'Ayuda de la tripulación'; const p = document.createElement('p'); p.textContent = hint.text; article.append(label, p); panel.append(article); });
    hintKey = key;
  }
  document.querySelector('#hint-count').textContent = game.hints.length;
  const help = document.querySelector('#help'); help.disabled = !game.playable || busy || game.help_pending;
  help.textContent = game.help_pending ? 'Ayuda solicitada' : 'Solicitar ayuda';
  document.querySelector('#help-status').textContent = game.help_pending ? 'Petición pendiente. Avisen al facilitador.' : '';
  document.querySelector('#locked-record').hidden = !!game.blocks;
  document.querySelector('#unlocked-record').hidden = !game.blocks;
  document.querySelector('#lock-icon').toggleAttribute('hidden', !!game.blocks);
  if (game.blocks && recordKey !== game.id) {
    document.querySelector('#binary-blocks').replaceChildren(...blockElements(game.blocks).children); recordKey = game.id;
  }
  document.querySelectorAll('#code-form input, #code-form button').forEach(el => { el.disabled = !game.playable || busy; });
  document.querySelector('#code-form').hidden = game.phase === 'RESUELTA';
}
export function initializeTable() {
  const rows = document.querySelector('#table-rows');
  for (let n = 0; n < 10; n++) {
    const row = document.createElement('tr');
    [String(n), n.toString(2).padStart(4, '0')].forEach(value => { const cell = document.createElement('td'); cell.textContent = value; row.append(cell); }); rows.append(row);
  }
  document.querySelector('#close-table').addEventListener('click', () => { document.querySelector('#binary-table').open = false; const input = document.querySelector('#message'); (input.disabled ? document.querySelector('summary') : input).focus(); });
}
