import { api } from './api.js';
import { crewName, crewTime, supportText } from './ranking-format.js';

const REFRESH_MS = 5000;
const list = document.querySelector('#ranking-list');
const empty = document.querySelector('#ranking-empty');
let signature = '';

function row(entry, index) {
  const item = document.createElement('li'); item.className = 'rank-row';
  const position = document.createElement('span'); position.className = 'rank-position'; position.textContent = String(index + 1).padStart(2, '0');
  const crew = document.createElement('div'); crew.className = 'rank-crew';
  const name = document.createElement('strong'); name.textContent = crewName(entry);
  const support = document.createElement('span'); support.textContent = supportText(entry);
  crew.append(name, support);
  const time = document.createElement('span'); time.className = 'rank-time'; time.textContent = crewTime(entry);
  item.append(position, crew, time);
  return item;
}

async function refresh() {
  try {
    const { entries } = await api('/api/ranking');
    const next = JSON.stringify(entries);
    if (next === signature) return;
    signature = next;
    list.replaceChildren(...entries.map(row));
    empty.hidden = entries.length > 0;
  } catch {
    empty.textContent = 'Sin conexión con la estación. Reintentando…'; empty.hidden = false;
  }
}

await refresh();
setInterval(refresh, REFRESH_MS);
