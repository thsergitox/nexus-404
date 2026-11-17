import { DURATION, poseAt } from './launch/trajectory.js';
import { drawFlame, drawShip, engineAt } from './launch/ship-renderer.js';
import { createTrail } from './launch/trail.js';

const FADE_MS = 600;
let running = false;

function createStage() {
  const stage = document.createElement('div'); stage.className = 'launch'; stage.setAttribute('aria-hidden', 'true');
  const canvas = document.createElement('canvas');
  const caption = document.createElement('div'); caption.className = 'launch-caption';
  const title = document.createElement('strong'); title.textContent = 'Salto iniciado';
  const subtitle = document.createElement('span'); subtitle.textContent = 'Rumbo a Nexus 150A';
  caption.append(title, subtitle); stage.append(canvas, caption);
  document.body.append(stage);
  return { stage, canvas };
}

function fitCanvas(canvas) {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  const width = window.innerWidth, height = window.innerHeight;
  canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio);
  const context = canvas.getContext('2d'); context.setTransform(ratio, 0, 0, ratio, 0, 0);
  return { context, width, height };
}

function drawWarpFlash(context, width, height, pose) {
  const alpha = Math.max(0, 1 - Math.abs(pose.warp - 0.85) * 5) * 0.55;
  if (alpha <= 0) return;
  context.fillStyle = `rgba(220,255,200,${alpha})`; context.fillRect(0, 0, width, height);
}

function frame(context, width, height, trail, elapsed, seconds) {
  context.clearRect(0, 0, width, height);
  trail.update(seconds);
  const pose = poseAt(elapsed, width, height);
  if (pose.visible) {
    const engine = engineAt(pose);
    trail.emit(engine.x, engine.y, Math.PI - pose.pitch, pose.flame);
  }
  trail.draw(context);
  if (pose.visible) { drawFlame(context, pose); drawShip(context, pose); }
  drawWarpFlash(context, width, height, pose);
}

export function launchShip() {
  if (running || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  running = true;
  const { stage, canvas } = createStage();
  let view = fitCanvas(canvas);
  const resize = () => { view = fitCanvas(canvas); };
  window.addEventListener('resize', resize);
  const trail = createTrail();
  const startedAt = performance.now();
  let previous = startedAt;

  function finish() {
    window.removeEventListener('resize', resize);
    stage.classList.add('leaving');
    setTimeout(() => { stage.remove(); running = false; }, FADE_MS);
  }

  function tick(now) {
    const elapsed = now - startedAt;
    frame(view.context, view.width, view.height, trail, elapsed, Math.min(0.05, (now - previous) / 1000));
    previous = now;
    if (elapsed < DURATION) requestAnimationFrame(tick); else finish();
  }
  requestAnimationFrame(tick);
}
