import { ENGINE, FACES, MATERIALS } from './ship-model.js';

const LIGHT = normalize([-0.35, 0.8, 0.5]);
const PERSPECTIVE = 0.16;
const VIEW_TILT = 0.38;

function normalize([x, y, z]) {
  const length = Math.hypot(x, y, z) || 1;
  return [x / length, y / length, z / length];
}

function cross(a, b) {
  return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
}

function orient([x, y, z], { roll, pitch, yaw, stretch }) {
  x *= stretch;
  const cr = Math.cos(roll), sr = Math.sin(roll);
  [y, z] = [y * cr - z * sr, y * sr + z * cr];
  const cp = Math.cos(pitch), sp = Math.sin(pitch);
  [x, y] = [x * cp - y * sp, x * sp + y * cp];
  const cy = Math.cos(yaw), sy = Math.sin(yaw);
  [x, z] = [x * cy + z * sy, -x * sy + z * cy];
  const ct = Math.cos(VIEW_TILT), st = Math.sin(VIEW_TILT);
  return [x, y * ct - z * st, y * st + z * ct];
}

function project([x, y, z], pose) {
  const scale = pose.size / (1 - z * PERSPECTIVE);
  return { x: pose.x + x * scale, y: pose.y - y * scale, depth: z };
}

function shade(material, normal) {
  const { color, glow } = MATERIALS[material];
  const light = Math.abs(normal[0] * LIGHT[0] + normal[1] * LIGHT[1] + normal[2] * LIGHT[2]);
  const brightness = Math.min(1.15, 0.28 + light * 0.8 + glow);
  return `rgb(${color.map(channel => Math.round(Math.min(255, channel * brightness))).join(',')})`;
}

function polygons(pose) {
  return FACES.map(({ material, points }) => {
    const world = points.map(point => orient(point, pose));
    const a = world[0], b = world[1], c = world[2];
    const normal = normalize(cross([b[0] - a[0], b[1] - a[1], b[2] - a[2]], [c[0] - a[0], c[1] - a[1], c[2] - a[2]]));
    const depth = world.reduce((sum, point) => sum + point[2], 0) / world.length;
    return { fill: shade(material, normal), depth, screen: world.map(point => project(point, pose)) };
  }).sort((first, second) => first.depth - second.depth);
}

export function engineAt(pose) {
  return project(orient(ENGINE, pose), pose);
}

export function drawFlame(context, pose) {
  if (pose.flame <= 0) return;
  const length = 0.5 + pose.flame * (1.3 + Math.random() * 0.45);
  const base = engineAt(pose);
  const tip = project(orient([ENGINE[0] - length, ENGINE[1], 0], pose), pose);
  const angle = Math.atan2(tip.y - base.y, tip.x - base.x);
  const width = pose.size * (0.12 + pose.flame * 0.08);
  const gradient = context.createLinearGradient(base.x, base.y, tip.x, tip.y);
  gradient.addColorStop(0, 'rgba(255,255,240,0.95)');
  gradient.addColorStop(0.25, 'rgba(198,243,107,0.85)');
  gradient.addColorStop(0.7, 'rgba(110,242,255,0.35)');
  gradient.addColorStop(1, 'rgba(110,242,255,0)');
  const px = -Math.sin(angle) * width, py = Math.cos(angle) * width;
  context.save(); context.globalCompositeOperation = 'lighter'; context.fillStyle = gradient;
  context.beginPath(); context.moveTo(base.x + px, base.y + py);
  context.quadraticCurveTo(base.x + (tip.x - base.x) * 0.35 + px * 0.9, base.y + (tip.y - base.y) * 0.35 + py * 0.9, tip.x, tip.y);
  context.quadraticCurveTo(base.x + (tip.x - base.x) * 0.35 - px * 0.9, base.y + (tip.y - base.y) * 0.35 - py * 0.9, base.x - px, base.y - py);
  context.closePath(); context.fill();
  const halo = context.createRadialGradient(base.x, base.y, 0, base.x, base.y, width * 2.6);
  halo.addColorStop(0, 'rgba(198,243,107,0.55)'); halo.addColorStop(1, 'rgba(198,243,107,0)');
  context.fillStyle = halo; context.beginPath(); context.arc(base.x, base.y, width * 2.6, 0, Math.PI * 2); context.fill();
  context.restore();
}

export function drawShip(context, pose) {
  context.save(); context.lineJoin = 'round'; context.lineWidth = 1;
  context.shadowColor = 'rgba(110,242,255,0.55)'; context.shadowBlur = pose.size * 0.25;
  for (const polygon of polygons(pose)) {
    context.beginPath();
    polygon.screen.forEach((point, index) => (index ? context.lineTo(point.x, point.y) : context.moveTo(point.x, point.y)));
    context.closePath(); context.fillStyle = polygon.fill; context.fill();
    context.strokeStyle = 'rgba(110,242,255,0.75)'; context.stroke();
  }
  context.restore();
}
