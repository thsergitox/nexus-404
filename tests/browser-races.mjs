import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

function element() {
  return { value: '', hidden: false, disabled: false, textContent: '',
    classList: { toggle() {} }, addEventListener() {}, replaceChildren() {},
    append() {}, focus() {} };
}

function harness(file) {
  const elements = new Map();
  const requests = [];
  const query = selector => {
    if (!elements.has(selector)) elements.set(selector, element());
    return elements.get(selector);
  };
  const source = readFileSync(new URL(`../web/${file}`, import.meta.url), 'utf8')
    .replace(/^import .*;\n/gm, '')
    .replace(/^await refresh\(\); setInterval[^\n]*/m, '');
  const context = vm.createContext({
    document: { querySelector: query, querySelectorAll: () => [],
      createElement: element, body: element() },
    api: (path, data) => new Promise((resolve, reject) => requests.push({ path, data, resolve, reject })),
    initializeTable() {}, initializeBriefing() {}, renderMessages() {}, renderPanels() {},
    noticeText: () => '', timeText: String,
    showError: (node, message = '') => { node.textContent = message; node.hidden = !message; },
    performance: { now: () => 0 },
  });
  const mutation = file === 'app.js'
    ? "perform('/api/help', {}, document.querySelector('#chat-error'))"
    : "control('reset', game.id)";
  vm.runInContext(`${source}\nglobalThis.exercise = {
    refresh, mutate: () => ${mutation}, getGame: () => game
  };`, context);
  return { ...context.exercise, requests, query };
}

function game(id, phase = 'PREPARADA') {
  return { id, phase, remaining: 900, playable: phase !== 'PREPARADA', mode: 'local',
    hints: [], messages: [], metrics: [], usage: { requests: 0, input_tokens: 0, output_tokens: 0 } };
}

async function initialize(h) {
  const refresh = h.refresh();
  h.requests.at(-1).resolve(game('initial'));
  await refresh;
}

for (const file of ['app.js', 'facilitator.js']) {
  test(`${file}: an older GET cannot restore the previous group`, async () => {
    const h = harness(file);
    const old = h.refresh();
    const fresh = h.refresh();
    h.requests[1].resolve(game('new-group'));
    await fresh;
    h.requests[0].resolve(game('old-group', 'REGISTRO_LIBERADO'));
    await old;
    assert.equal(h.getGame().id, 'new-group');
  });

  test(`${file}: a completed mutation invalidates an earlier GET`, async () => {
    const h = harness(file);
    await initialize(h);
    const stale = h.refresh();
    const mutation = h.mutate();
    h.requests[2].resolve(game('after-mutation'));
    await mutation;
    h.requests[1].resolve(game('initial'));
    await stale;
    assert.equal(h.getGame().id, 'after-mutation');
  });

  test(`${file}: polling stays idle during a mutation`, async () => {
    const h = harness(file);
    await initialize(h);
    const mutation = h.mutate();
    await h.refresh();
    assert.equal(h.requests.length, 2);
    h.requests[1].resolve(game('after-mutation'));
    await mutation;
  });
}
