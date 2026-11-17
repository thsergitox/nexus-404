import { api } from './api.js';
import { createNoteCard } from './note-card.js';
import { createNoteViewer } from './note-viewer.js';

export async function initializeBriefing() {
  const file = document.querySelector('#crew-file');
  document.querySelector('#briefing-shortcut').addEventListener('click', () => {
    file.open = true; file.scrollIntoView({ block: 'start' }); file.querySelector('summary').focus();
  });
  file.addEventListener('toggle', () => { if (file.open) file.classList.add('seen'); });
  const container = document.querySelector('#crew-notes');
  const viewer = createNoteViewer(document.querySelector('#note-dialog'));
  try {
    const { notes } = await api('/api/briefing');
    container.append(...notes.map(note => createNoteCard(note, viewer.open)));
  } catch {
    container.textContent = 'No se pudo cargar el expediente. Pidan al facilitador las cuatro notas impresas.';
  }
}
