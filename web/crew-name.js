import { api, showError } from './api.js';

const $ = selector => document.querySelector(selector);

export function renderCrewName(game) {
  $('#crew-name-form').hidden = game.crew_named !== false;
  $('#crew-name-done').hidden = game.crew_named !== true;
}

export function initializeCrewName(currentGame, onRegistered) {
  const form = $('#crew-name-form'), button = form.querySelector('button'), error = $('#crew-name-error');
  form.addEventListener('submit', async event => {
    event.preventDefault();
    button.disabled = true; showError(error);
    try { onRegistered(await api('/api/ranking/name', { game_id: currentGame().id, name: $('#crew-name').value })); }
    catch (failure) { showError(error, failure.message); }
    finally { button.disabled = false; }
  });
}
