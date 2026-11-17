import { api, showError } from './api.js';
import { discardPendingMessage, noticeText, renderMessages, showPendingMessage, timeText } from './render.js';
import { initializeTable, renderPanels } from './panels.js';
import { initializeBriefing } from './briefing.js';
import { launchShip } from './launch.js';
import { initializeCrewName, renderCrewName } from './crew-name.js';
const $ = selector => document.querySelector(selector);
let game, busy = false, syncedAt = 0, connected = false, retryMessage;
let requestSequence = 0, appliedSequence = 0;
const memory = { id: null, count: 0 };
const STATION_SECONDS = 900;
initializeTable();
initializeBriefing();
initializeCrewName(() => game, next => { appliedSequence = ++requestSequence; display(next); });
function display(next) {
  if (game && game.id !== next.id) {
    $('#message').value = ''; $('#code').value = ''; $('#count').textContent = '0 / 800'; retryMessage = null;
    $('#binary-table').open = false; showError($('#code-error')); showError($('#chat-error'));
    $('#crew-file').open = false; $('#crew-file').classList.remove('seen'); $('#crew-name').value = '';
  }
  const solvedNow = game?.id === next.id && game.phase !== 'RESUELTA' && next.phase === 'RESUELTA';
  game = next; syncedAt = performance.now(); connected = true;
  renderMessages($('#messages'), game, memory, $('#new-messages'));
  renderPanels(game, busy); renderCrewName(game); document.body.classList.toggle('won', game.phase === 'RESUELTA');
  const notice = noticeText(game); $('#notice').textContent = notice; $('#notice').hidden = !notice;
  $('#notice').classList.toggle('success', game.phase === 'RESUELTA');
  $('#message').disabled = !game.playable || busy || game.pending;
  $('#send').disabled = !game.playable || busy || game.pending;
  $('#thinking').hidden = !(busy || game.pending);
  $('#chat-state').textContent = busy || game.pending ? 'Recibiendo señal' : game.playable ? 'Canal abierto' : 'En espera';
  document.body.classList.toggle('receiving', busy || game.pending);
  $('#connection-label').textContent = game.mode === 'local' ? 'NORA · contingencia local' : 'NORA · enlace conectado';
  $('#mode-label').textContent = game.mode === 'local' ? 'Contingencia local' : 'Conversación con OpenAI';
  updateClock();
  if (solvedNow) launchShip();
}
function updateClock() {
  if (!game) return;
  const running = game.playable && connected;
  const seconds = game.remaining - (running ? (performance.now() - syncedAt) / 1000 : 0);
  $('#clock').textContent = timeText(seconds); $('.timer').classList.toggle('urgent', seconds < 120);
  $('.timer').style.setProperty('--progress', Math.max(0, Math.min(1, seconds / Math.max(STATION_SECONDS, game.remaining))));
  document.body.classList.toggle('red-alert', running && seconds < 120 && seconds > 0);
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
  const sentFor = game.id;
  showPendingMessage($('#messages'), memory, text);
  $('#message').value = ''; $('#count').textContent = '0 / 800';
  const success = await perform('/api/chat', { text, message_id: retryMessage.message_id }, $('#chat-error'));
  if (success) { retryMessage = null; if (!$('#message').disabled) $('#message').focus(); return; }
  discardPendingMessage(memory);
  if (game?.id === sentFor) { $('#message').value = text; $('#count').textContent = `${text.length} / 800`; }
}
$('#chat-form').addEventListener('submit', sendMessage);
$('#message').addEventListener('keydown', event => { if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); $('#chat-form').requestSubmit(); } });
$('#message').addEventListener('input', () => { $('#count').textContent = `${$('#message').value.length} / 800`; });
$('#help').addEventListener('click', () => perform('/api/help', {}, $('#chat-error')));
$('#code-form').addEventListener('submit', event => { event.preventDefault(); perform('/api/validate', { code: $('#code').value }, $('#code-error')); });
$('#new-messages').addEventListener('click', () => { $('#messages').scrollTop = $('#messages').scrollHeight; $('#new-messages').hidden = true; });
$('#messages').addEventListener('scroll', () => { if ($('#messages').scrollHeight - $('#messages').scrollTop - $('#messages').clientHeight < 70) $('#new-messages').hidden = true; });
await refresh(); setInterval(refresh, 1800); setInterval(updateClock, 250);
