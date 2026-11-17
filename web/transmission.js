const BASE_CPS = 48;
const MAX_SECONDS = 7;
const NOISE_WIDTH = 7;
const GLYPHS = '▓▒░<>/\\|=+*#ΔΣΞΛ◇◆¦';

function revealCount(length, elapsedMs) {
  const charsPerSecond = Math.max(BASE_CPS, length / MAX_SECONDS);
  return Math.min(length, Math.floor((elapsedMs / 1000) * charsPerSecond));
}

function noiseFor(text, from) {
  return [...text.slice(from, from + NOISE_WIDTH)]
    .map(char => (/\s/.test(char) ? char : GLYPHS[Math.floor(Math.random() * GLYPHS.length)]))
    .join('');
}

export function transmit(target, text, { onFrame = () => {}, reduced = false } = {}) {
  return new Promise(resolve => {
    if (reduced || !text) { target.textContent = text; resolve(); return; }
    const settled = document.createTextNode('');
    const noise = document.createElement('span'); noise.className = 'tx-noise';
    const cursor = document.createElement('span'); cursor.className = 'tx-cursor';
    target.replaceChildren(settled, noise, cursor);
    const start = performance.now();
    const frame = now => {
      if (!target.isConnected) { resolve(); return; }
      const shown = revealCount(text.length, now - start);
      settled.data = text.slice(0, shown);
      noise.textContent = noiseFor(text, shown);
      onFrame();
      if (shown < text.length) { requestAnimationFrame(frame); return; }
      target.textContent = text; onFrame(); resolve();
    };
    requestAnimationFrame(frame);
  });
}
