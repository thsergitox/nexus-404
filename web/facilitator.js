import { api, showError } from './api.js';
import { timeText } from './render.js';
import { createRankingAdmin } from './facilitator-ranking.js';
const $ = selector => document.querySelector(selector);
let game, busy = false, hintSignature = '';
let requestSequence = 0, appliedSequence = 0;
const ranking = createRankingAdmin({ onError: message => showError($('#admin-error'), message), onFeedback: message => showError($('#admin-feedback'), message) });
const phases = { PREPARADA: 'Preparada', EN_CURSO: 'En conversación', MANTENIMIENTO: 'Mantenimiento activo', REGISTRO_LIBERADO: 'Registro recuperado', RESUELTA: 'Navegación restaurada', AGOTADA: 'Tiempo agotado' };
const reasons = { missing_key: 'Falta OPENAI_API_KEY en el servidor.', connection: 'No se pudo comunicar con OpenAI.', timeout: 'OpenAI superó el plazo de respuesta.', invalid_output: 'La salida del modelo no superó la validación.', token_limit: 'Se alcanzó el tope del evento. Contingencia activada; reanude para continuar.', refusal: 'El modelo rechazó responder.', incomplete: 'OpenAI devolvió una respuesta incompleta.' };
function render(next) {
  game = next; $('#login-panel').hidden = true; $('#dashboard').hidden = false;
  $('#phase').textContent = phases[game.phase]; $('#clock').textContent = timeText(game.remaining);
  $('#conditions').textContent = `${game.paused ? 'En pausa' : game.playable ? 'Reloj en marcha' : 'Reloj detenido'} · ${game.mode === 'local' ? 'Contingencia local' : 'Generativo por OpenAI'}`;
  $('#technical').hidden = !game.technical_reason;
  $('#technical').textContent = `${reasons[game.technical_reason] || 'Interrupción técnica: revise la configuración.'} El progreso se conserva.`;
  $('#provider-info').textContent = `Modelo: ${game.model} · ${game.api_configured ? 'Clave configurada (acceso por verificar)' : 'Sin API key'} · ${game.strict_catalog ? 'Catálogo estricto' : 'Redacción generativa habilitada'}`;
  $('#help-pending').hidden = !game.help_pending;
  const active = ['EN_CURSO', 'MANTENIMIENTO', 'REGISTRO_LIBERADO'].includes(game.phase);
  $('[data-action="start"]').disabled = busy || game.phase !== 'PREPARADA';
  $('[data-action="pause"]').disabled = busy || !active || game.paused;
  $('[data-action="resume"]').disabled = busy || !active || !game.paused;
  $('[data-action="release"]').disabled = busy || !active || !!game.blocks;
  $('#extend-form button').disabled = busy || (!active && game.phase !== 'AGOTADA');
  document.querySelectorAll('[data-mode]').forEach(button => { button.disabled = busy || button.dataset.mode === game.mode; });
  $('#reset').disabled = busy;
  renderHints(active); renderMetrics();
}
function renderHints(active) {
  if (!game.hint_catalog) return;
  const signature = game.id + JSON.stringify(game.hints) + game.phase + busy;
  if (signature === hintSignature) return;
  hintSignature = signature;
  const controls = $('#hint-controls'); controls.replaceChildren();
  Object.entries(game.hint_catalog).forEach(([id, text]) => {
    const row = document.createElement('div'); row.className = 'hint-control';
    const content = document.createElement('div'); const label = document.createElement('strong'); label.textContent = id;
    const p = document.createElement('p'); p.textContent = text; content.append(label, p);
    const button = document.createElement('button'); button.className = 'secondary';
    const released = game.hints.some(h => h.id === id); button.textContent = released ? 'Liberada' : `Liberar ${id}`;
    button.disabled = busy || released || !active || (id.startsWith('B') && !game.blocks);
    button.addEventListener('click', () => control('hint', id)); row.append(content, button); controls.append(row);
  });
}
function renderMetrics() {
  const metrics = $('#metrics'); metrics.replaceChildren();
  const values = { 'Peticiones a OpenAI': game.usage.requests, 'Tokens de este grupo': game.usage.input_tokens + game.usage.output_tokens,
    'Tokens del evento': game.event_tokens, 'Tope propio del evento': game.token_limit || 'Sin configurar',
    'Ayudas liberadas': game.hints.length, 'Asistencia directa': game.assisted ? 'Sí' : 'No', 'Prompt': game.prompt_version };
  Object.entries(values).forEach(([name, value]) => { const dt = document.createElement('dt'); dt.textContent = name; const dd = document.createElement('dd'); dd.textContent = value; metrics.append(dt, dd); });
  const past = $('#past-metrics'); past.replaceChildren();
  if (!game.metrics.length) past.textContent = 'Todavía no se ha reiniciado ningún grupo.';
  game.metrics.forEach((entry, i) => { const p = document.createElement('p'); p.className = 'metric-row'; p.textContent = `Grupo ${i + 1}: ${phases[entry.result]} · ${entry.turns} turnos · ${entry.hints.length} ayudas · ${entry.assisted ? 'con asistencia directa' : 'sin asistencia directa'}`; past.append(p); });
}
async function refresh() {
  if (busy) return;
  const sequence = ++requestSequence;
  try { const next = await api('/api/admin/state'); if (!busy && sequence > appliedSequence) { appliedSequence = sequence; render(next); ranking.refresh(); } }
  catch (error) { if (sequence < appliedSequence || busy) return; if (error.status === 401) { $('#login-panel').hidden = false; $('#dashboard').hidden = true; game = null; } else showError($('#admin-error'), error.message); }
}
async function control(action, value) {
  if (!game || busy) return;
  const catalog = game.hint_catalog;
  busy = true; const sequence = ++requestSequence; render(game); showError($('#admin-error')); showError($('#admin-feedback'));
  try { const next = await api('/api/admin/control', { game_id: game.id, action, value }); busy = false; appliedSequence = sequence; render({ ...next, hint_catalog: catalog }); showError($('#admin-feedback'), 'Acción aplicada y guardada en la estación.'); }
  catch (error) { busy = false; showError($('#admin-error'), error.message); await refresh(); }
}
$('#login-form').addEventListener('submit', async event => {
  event.preventDefault(); const button = $('#login-form button'); button.disabled = true;
  try { await api('/api/admin/login', { password: $('#password').value }); $('#password').value = ''; showError($('#admin-error')); await refresh(); }
  catch (error) { showError($('#admin-error'), error.message); }
  finally { button.disabled = false; }
});
document.querySelectorAll('[data-action]').forEach(button => button.addEventListener('click', () => control(button.dataset.action)));
document.querySelectorAll('[data-mode]').forEach(button => button.addEventListener('click', () => control('mode', button.dataset.mode)));
$('#extend-form').addEventListener('submit', event => { event.preventDefault(); control('extend', Number($('#seconds').value)); });
$('#reset').addEventListener('click', () => $('#reset-dialog').showModal());
$('#reset-dialog').addEventListener('close', () => { if ($('#reset-dialog').returnValue === 'confirm') control('reset', game.id); });
$('#logout').addEventListener('click', async () => { try { await api('/api/admin/logout', {}); appliedSequence = ++requestSequence; $('#dashboard').hidden = true; $('#login-panel').hidden = false; game = null; hintSignature = ''; $('#hint-controls').replaceChildren(); showError($('#admin-feedback')); } catch (error) { showError($('#admin-error'), error.message); } });
await refresh(); setInterval(refresh, 1800);
