import { createMessage, prepareForTransmission } from './message-view.js';
import { transmit } from './transmission.js';

const STICK_DISTANCE = 140;
const reducedMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const distanceToBottom = container => container.scrollHeight - container.scrollTop - container.clientHeight;
const scrollToBottom = container => { container.scrollTop = container.scrollHeight; };

export function showPendingMessage(container, memory, text) {
  discardPendingMessage(memory);
  const element = createMessage({ role: 'user', text });
  element.classList.add('pending');
  container.append(element); scrollToBottom(container);
  memory.pending = { element, text: text.trim() };
}

export function discardPendingMessage(memory) {
  memory.pending?.element.remove();
  memory.pending = null;
}

function adoptsPending(memory, message) {
  return memory.pending && message.role === 'user' && message.text === memory.pending.text;
}

function queueTransmission(container, article, text, memory, newButton) {
  const { visible, card } = prepareForTransmission(article, text);
  article.classList.add('queued');
  const follow = () => {
    if (distanceToBottom(container) < STICK_DISTANCE) scrollToBottom(container);
    else newButton.hidden = false;
  };
  memory.queue = (memory.queue || Promise.resolve()).then(() => {
    article.classList.replace('queued', 'streaming');
    return transmit(visible, text, { onFrame: follow, reduced: reducedMotion() });
  }).then(() => {
    article.classList.remove('streaming'); article.classList.add('received');
    if (card) { card.hidden = false; follow(); }
  });
}

export function renderMessages(container, game, memory, newButton) {
  const nearBottom = distanceToBottom(container) < 70;
  const fresh = memory.id !== game.id;
  if (fresh) {
    container.replaceChildren();
    Object.assign(memory, { id: game.id, count: 0, pending: null, queue: null });
  }
  const added = game.messages.slice(memory.count);
  added.forEach(message => {
    if (adoptsPending(memory, message)) {
      memory.pending.element.classList.remove('pending'); memory.pending = null; return;
    }
    const article = createMessage(message, game.blocks);
    container.insertBefore(article, memory.pending?.element ?? null);
    if (!fresh && message.role === 'assistant') queueTransmission(container, article, message.text, memory, newButton);
    else if (!fresh) article.classList.add('arrived');
  });
  memory.count = game.messages.length;
  if (fresh || nearBottom) scrollToBottom(container);
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
