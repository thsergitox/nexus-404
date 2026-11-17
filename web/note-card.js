export function createNoteCard(note, onOpen) {
  const card = document.createElement('button');
  card.type = 'button'; card.className = 'note-card';
  card.setAttribute('aria-haspopup', 'dialog');
  card.setAttribute('aria-label', `Ampliar fragmento ${note.id}: ${note.title}`);

  const badge = document.createElement('span'); badge.className = 'note-badge'; badge.textContent = note.id;
  const title = document.createElement('h4'); title.textContent = note.title;
  const excerpt = document.createElement('p'); excerpt.textContent = note.text;
  const footer = document.createElement('span'); footer.className = 'note-footer';
  const author = document.createElement('span'); author.textContent = note.author;
  const cue = document.createElement('span'); cue.className = 'note-cue'; cue.textContent = 'Ampliar';
  footer.append(author, cue);

  card.append(badge, title, excerpt, footer);
  card.addEventListener('click', () => onOpen(note, card));
  return card;
}
