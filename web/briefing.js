import { api } from './api.js';

export async function initializeBriefing() {
  document.querySelector('#briefing-shortcut').addEventListener('click', () => {
    const file = document.querySelector('#crew-file'); file.open = true;
    file.scrollIntoView({ block: 'start' }); file.querySelector('summary').focus();
  });
  const container = document.querySelector('#crew-notes');
  try {
    const { notes } = await api('/api/briefing');
    notes.forEach(note => {
      const article = document.createElement('article');
      const title = document.createElement('h4'); title.textContent = note.title;
      const text = document.createElement('p'); text.textContent = note.text;
      const author = document.createElement('span'); author.textContent = `${note.author} · Fragmento ${note.id}`;
      article.append(title, text, author); container.append(article);
    });
  } catch {
    container.textContent = 'No se pudo cargar el expediente. Pidan al facilitador las cuatro notas impresas.';
  }
}
