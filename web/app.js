import { api, showError } from './api.js';
import { noticeText, renderMessages, timeText } from './render.js';
import { initializeTable, renderPanels } from './panels.js';
import { initializeBriefing } from './briefing.js';
const $ = selector => document.querySelector(selector);
let game, busy = false, syncedAt = 0, connected = false, retryMessage;
let requestSequence = 0, appliedSequence = 0;
const memory = { id: null, count: 0 };
initializeTable();
initializeBriefing();
function display(next) {
  if (game && game.id !== next.id) {
    $('#message').value = ''; $('#code').value = ''; $('#count').textContent = '0 / 800'; retryMessage = null;
    $('#binary-table').open = false; showError($('#code-error')); showError($('#chat-error'));
  }
  game = next; syncedAt = performance.now(); connected = true;
  renderMessages($('#messages'), game, memory, $('#new-messages'));
  renderPanels(game, busy); document.body.classList.toggle('won', game.phase === 'RESUELTA');
  const notice = noticeText(game); $('#notice').textContent = notice; $('#notice').hidden = !notice;
  $('#notice').classList.toggle('success', game.phase === 'RESUELTA');
  $('#message').disabled = !game.playable || busy || game.pending;
  $('#send').disabled = !game.playable || busy || game.pending;
  $('#thinking').hidden = !(busy || game.pending);
  $('#chat-state').textContent = busy || game.pending ? 'Respondiendo' : game.playable ? 'Canal abierto' : 'En espera';
  $('#connection-label').textContent = game.mode === 'local' ? 'NORA · contingencia local' : 'NORA · enlace conectado';
  $('#mode-label').textContent = game.mode === 'local' ? 'Contingencia local' : 'Conversación con OpenAI';
  updateClock();
}
function updateClock() {
  if (!game) return;
  const running = game.playable && connected;
  const seconds = game.remaining - (running ? (performance.now() - syncedAt) / 1000 : 0);
  $('#clock').textContent = timeText(seconds); $('.timer').classList.toggle('urgent', seconds < 120);
  if (seconds <= 0 && running) { $('#send').disabled = true; $('#message').disabled = true; }
}
async function refresh() {
  if (busy) return;
  const sequence = ++requestSequence;
  try {
    const next = await api('/api/state');
    if (!busy && sequence > appliedSequence) { appliedSequence = sequence; display(next); }
  } catch (error) {
    if (sequence < appliedSequence || busy) return;
    connected = false; $('#notice').hidden = false; $('#notice').textContent = error.message;
    $('#send').disabled = true; $('#message').disabled = true;
  }
}
async function perform(path, data, errorElement) {
  if (!game || busy) return;
  busy = true; const sequence = ++requestSequence; showError(errorElement); display(game);
  try { const next = await api(path, { game_id: game.id, ...data }); busy = false; appliedSequence = sequence; display(next); return true; }
  catch (error) { busy = false; await refresh(); showError(errorElement, error.message); return false; }
}
async function sendMessage(event) {
  event.preventDefault();
  const text = $('#message').value.trim();
  if (!text || !game?.playable || busy) return;
  if (!retryMessage || retryMessage.text !== text || retryMessage.game !== game.id) retryMessage = { text, message_id: crypto.randomUUID(), game: game.id };
  const success = await perform('/api/chat', { text, message_id: retryMessage.message_id }, $('#chat-error'));
  if (success) { $('#message').value = ''; retryMessage = null; $('#count').textContent = '0 / 800'; if (!$('#message').disabled) $('#message').focus(); }
}
$('#chat-form').addEventListener('submit', sendMessage);
$('#message').addEventListener('keydown', event => { if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); $('#chat-form').requestSubmit(); } });
$('#message').addEventListener('input', () => { $('#count').textContent = `${$('#message').value.length} / 800`; });
$('#help').addEventListener('click', () => perform('/api/help', {}, $('#chat-error')));
$('#code-form').addEventListener('submit', event => { event.preventDefault(); perform('/api/validate', { code: $('#code').value }, $('#code-error')); });
$('#new-messages').addEventListener('click', () => { $('#messages').scrollTop = $('#messages').scrollHeight; $('#new-messages').hidden = true; });
$('#messages').addEventListener('scroll', () => { if ($('#messages').scrollHeight - $('#messages').scrollTop - $('#messages').clientHeight < 70) $('#new-messages').hidden = true; });
await refresh(); setInterval(refresh, 1800); setInterval(updateClock, 250);
