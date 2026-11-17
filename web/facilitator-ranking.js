import { api } from './api.js';
import { crewName, crewTime, supportText } from './ranking-format.js';

const $ = selector => document.querySelector(selector);
const clock = new Intl.DateTimeFormat('es', { hour: '2-digit', minute: '2-digit' });

function cell(text, className) {
  const td = document.createElement('td'); td.textContent = text; if (className) td.className = className; return td;
}

export function createRankingAdmin({ onError, onFeedback }) {
  const selected = new Set();
  let signature = '';

  function syncDeleteButton() {
    $('#ranking-delete').disabled = selected.size === 0;
    $('#ranking-delete').textContent = selected.size ? `Eliminar seleccionados (${selected.size})` : 'Eliminar seleccionados';
  }

  function row(entry, index) {
    const tr = document.createElement('tr');
    const pick = document.createElement('td'); const box = document.createElement('input');
    box.type = 'checkbox'; box.checked = selected.has(entry.id);
    box.setAttribute('aria-label', `Seleccionar ${crewName(entry)}, ${crewTime(entry)}`);
    box.addEventListener('change', () => { box.checked ? selected.add(entry.id) : selected.delete(entry.id); syncDeleteButton(); });
    pick.append(box);
    tr.append(pick, cell(String(index + 1)), cell(crewName(entry), entry.name ? '' : 'muted'), cell(crewTime(entry), 'rank-admin-time'),
      cell(supportText(entry), 'small muted'), cell(clock.format(new Date(entry.finished * 1000)), 'small muted'));
    return tr;
  }

  function render(entries) {
    const next = JSON.stringify(entries);
    if (next === signature) return;
    signature = next;
    const ids = new Set(entries.map(entry => entry.id));
    [...selected].forEach(id => { if (!ids.has(id)) selected.delete(id); });
    $('#ranking-rows').replaceChildren(...entries.map(row));
    $('#ranking-admin-empty').hidden = entries.length > 0;
    $('#ranking-clear').disabled = entries.length === 0;
    syncDeleteButton();
  }

  async function mutate(path, data, message) {
    try { render((await api(path, data)).entries); onFeedback(message); }
    catch (error) { onError(error.message); }
  }

  async function refresh() {
    try { render((await api('/api/admin/ranking')).entries); } catch { /* el panel principal ya informa la desconexión */ }
  }

  $('#ranking-delete').addEventListener('click', () => {
    const ids = [...selected];
    mutate('/api/admin/ranking/delete', { ids }, ids.length === 1 ? 'Tiempo eliminado del ranking.' : `${ids.length} tiempos eliminados del ranking.`);
  });
  $('#ranking-clear').addEventListener('click', () => $('#ranking-clear-dialog').showModal());
  $('#ranking-clear-dialog').addEventListener('close', () => {
    if ($('#ranking-clear-dialog').returnValue === 'confirm') mutate('/api/admin/ranking/clear', { confirm: true }, 'Ranking vaciado.');
  });

  return { refresh };
}
