const AUTHORS = { user: 'Tripulación', assistant: 'NORA', system: 'Sistema de navegación' };
const CHANNELS = { user: 'TX · puente', assistant: 'RX · transmisión entrante', system: 'Registro de a bordo' };

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function blockElements(blocks, className = 'chat-card') {
  const container = element('div', className);
  blocks.forEach(block => container.append(element('code', '', block)));
  return container;
}

function avatarFor(role) {
  const avatar = element('div', 'message-avatar'); avatar.setAttribute('aria-hidden', 'true');
  if (role === 'assistant') avatar.append(element('span', 'holo-ring'), element('span', 'holo-ring'), element('span', 'holo-dot'));
  else avatar.textContent = 'TX';
  return avatar;
}

function headerFor(role) {
  const header = element('header', 'message-header');
  header.append(element('span', 'message-author', AUTHORS[role]), element('span', 'message-channel', CHANNELS[role]));
  if (role === 'assistant') {
    const signal = element('span', 'signal'); signal.setAttribute('aria-hidden', 'true');
    for (let bar = 0; bar < 4; bar++) signal.append(element('i'));
    header.append(signal);
  }
  return header;
}

export function createMessage(message, blocks) {
  const article = element('article', `message ${message.role}`);
  const body = element('div', 'message-body');
  body.append(headerFor(message.role), element('p', 'message-text', message.text));
  if (message.card && blocks) body.append(blockElements(blocks));
  if (message.role !== 'system') article.append(avatarFor(message.role));
  article.append(body);
  return article;
}

export function prepareForTransmission(article, text) {
  const visible = article.querySelector('.message-text');
  visible.setAttribute('aria-hidden', 'true'); visible.textContent = '';
  const spoken = element('span', 'sr-only', text);
  visible.after(spoken);
  const card = article.querySelector('.chat-card');
  if (card) card.hidden = true;
  return { visible, card };
}
