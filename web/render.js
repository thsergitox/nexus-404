const roles = { user: 'Tripulación', assistant: 'NORA', system: 'Sistema de navegación' };
export function blockElements(blocks, className = 'chat-card') {
  const container = document.createElement('div'); container.className = className;
  blocks.forEach(block => { const code = document.createElement('code'); code.textContent = block; container.append(code); });
  return container;
}
export function createMessage(message, blocks) {
  const article = document.createElement('article'); article.className = `message ${message.role}`;
  const avatar = document.createElement('div'); avatar.className = 'message-avatar'; avatar.textContent = message.role === 'user' ? 'T' : 'N'; avatar.setAttribute('aria-hidden', 'true');
  const body = document.createElement('div'); body.className = 'message-body';
  const author = document.createElement('span'); author.className = 'message-author'; author.textContent = roles[message.role];
  const text = document.createElement('p'); text.textContent = message.text;
  body.append(author, text);
  if (message.card && blocks) body.append(blockElements(blocks));
  article.append(avatar, body); return article;
}
export function renderMessages(container, game, memory, newButton) {
  const nearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 70;
  const fresh = memory.id !== game.id;
  if (fresh) { container.replaceChildren(); memory.id = game.id; memory.count = 0; }
  const added = game.messages.slice(memory.count);
  added.forEach(message => container.append(createMessage(message, game.blocks)));
  memory.count = game.messages.length;
  if (fresh || nearBottom) container.scrollTop = container.scrollHeight;
  else if (added.length) newButton.hidden = false;
}
export function timeText(seconds) {
  const safe = Math.max(0, Math.ceil(seconds));
  return `${String(Math.floor(safe / 60)).padStart(2, '0')}:${String(safe % 60).padStart(2, '0')}`;
}
export function noticeText(game) {
  if (game.phase === 'RESUELTA') return 'Trayectoria restaurada. Avisen al facilitador para recibir el siguiente elemento de la misión.';
  if (game.phase === 'AGOTADA') return 'Tiempo de esta estación agotado. El progreso se conserva. Avisen al facilitador.';
  if (game.technical) return 'La comunicación se interrumpió. El juego está en pausa y el progreso se conserva. Avisen al facilitador.';
  if (game.paused) return 'Estación en pausa. El progreso y el tiempo se conservan.';
  if (game.phase === 'PREPARADA') return 'Todo listo para la misión. El facilitador iniciará el tiempo de la estación.';
  return '';
}
