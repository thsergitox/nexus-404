import { createStarfield } from './space/starfield.js';
import { createPlanet } from './space/planet.js';

const PALETTES = {
  cruise: { star: '214,236,255', warm: '255,214,170', line: '110,242,255', beacon: '198,243,107',
    surfaceLight: 'rgba(22,52,78,0.96)', surfaceDark: 'rgba(3,8,16,0.98)' },
  alert: { star: '255,214,214', warm: '255,170,150', line: '255,96,112', beacon: '255,181,71',
    surfaceLight: 'rgba(70,20,30,0.96)', surfaceDark: 'rgba(10,3,6,0.98)' },
  jump: { star: '230,255,200', warm: '200,250,255', line: '198,243,107', beacon: '110,242,255',
    surfaceLight: 'rgba(30,62,40,0.96)', surfaceDark: 'rgba(3,10,6,0.98)' },
};
const SPEED = { cruise: 0.018, alert: 0.035, jump: 1.4, coast: 0.16 };
const JUMP_MS = 5200;

function mode(body) {
  if (body.classList.contains('won')) return 'jump';
  if (body.classList.contains('red-alert')) return 'alert';
  return 'cruise';
}

function start(canvas) {
  const context = canvas.getContext('2d');
  const stars = createStarfield();
  const planet = createPlanet();
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const parallax = { x: 0, y: 0 }, target = { x: 0, y: 0 };
  let width = 0, height = 0, last = performance.now(), speed = SPEED.cruise, jumpedAt = null, frame = null;

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
    width = window.innerWidth; height = window.innerHeight;
    canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    if (reduced.matches) render(performance.now());
  }

  function targetSpeed(current, now) {
    if (current !== 'jump') { jumpedAt = null; return SPEED[current]; }
    jumpedAt ??= now;
    return now - jumpedAt < JUMP_MS ? SPEED.jump : SPEED.coast;
  }

  function render(now) {
    const delta = Math.min(0.05, (now - last) / 1000); last = now;
    const current = mode(document.body);
    speed += (targetSpeed(current, now) - speed) * Math.min(1, delta * 1.6);
    parallax.x += (target.x - parallax.x) * 0.04; parallax.y += (target.y - parallax.y) * 0.04;
    const palette = PALETTES[current];
    context.clearRect(0, 0, width, height);
    stars.draw(context, width, height, { speed: reduced.matches ? 0 : speed, delta, parallax, palette });
    planet.draw(context, width, height, { time: reduced.matches ? 0 : now, palette });
  }

  function loop(now) {
    render(now);
    frame = requestAnimationFrame(loop);
  }

  function run() {
    cancelAnimationFrame(frame); frame = null;
    if (reduced.matches || document.hidden) { render(performance.now()); return; }
    last = performance.now(); frame = requestAnimationFrame(loop);
  }

  window.addEventListener('resize', resize);
  window.addEventListener('pointermove', event => {
    target.x = event.clientX / window.innerWidth - 0.5; target.y = event.clientY / window.innerHeight - 0.5;
  }, { passive: true });
  document.addEventListener('visibilitychange', run);
  reduced.addEventListener('change', run);
  resize(); run();
}

const canvas = document.querySelector('#space');
if (canvas?.getContext) start(canvas);
