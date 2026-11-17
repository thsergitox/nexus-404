const IGNITION_MS = 700;
const FLIGHT_MS = 4600;
const WARP_MS = 700;
export const DURATION = FLIGHT_MS + WARP_MS + 1100;

const PATH = [[0.08, 1.15], [0.12, 0.28], [0.5, 0.42], [0.8, 0.42]];
const WARP_TARGET_X = 1.7;

const clamp = value => Math.max(0, Math.min(1, value));
const smooth = u => u * u * (3 - 2 * u);

function bezier(u) {
  const v = 1 - u;
  const weights = [v * v * v, 3 * v * v * u, 3 * v * u * u, u * u * u];
  return PATH.reduce(([x, y], point, index) => [x + point[0] * weights[index], y + point[1] * weights[index]], [0, 0]);
}

// Lento al despegar, rápido a mitad de vuelo y casi suspendido antes del salto.
function flightProgress(ms) {
  const u = clamp(ms / FLIGHT_MS);
  return u - 0.9 * Math.sin(2 * Math.PI * u) / (2 * Math.PI);
}

function positionAt(ms) {
  if (ms <= FLIGHT_MS) return bezier(flightProgress(ms));
  const v = clamp((ms - FLIGHT_MS) / WARP_MS);
  const [x, y] = PATH[3];
  return [x + (WARP_TARGET_X - x) * v ** 3, y];
}

function flameAt(ms) {
  if (ms < IGNITION_MS) return (ms / IGNITION_MS) * (0.4 + Math.random() * 0.4);
  if (ms > FLIGHT_MS) return 1.8;
  const u = ms / FLIGHT_MS;
  return 0.95 - u * 0.4;
}

function rollAt(ms) {
  const u = ms / FLIGHT_MS;
  const barrel = smooth(clamp((u - 0.42) / 0.3)) * Math.PI * 2;
  return barrel + Math.sin(u * Math.PI * 2) * 0.25;
}

export function poseAt(ms, width, height) {
  const base = Math.min(width, height) * 0.11;
  const [x, y] = positionAt(ms);
  const [nx, ny] = positionAt(Math.min(ms + 24, FLIGHT_MS + WARP_MS));
  const pitch = Math.atan2(-(ny - y) * height, (nx - x) * width) || 0;
  const u = clamp(ms / FLIGHT_MS);
  const shake = ms < IGNITION_MS + 400 ? (1 - ms / (IGNITION_MS + 400)) * 3 : 0;
  const warp = clamp((ms - FLIGHT_MS) / WARP_MS);
  return {
    x: x * width + (Math.random() - 0.5) * shake, y: y * height + (Math.random() - 0.5) * shake,
    size: base * (0.7 + Math.sin(Math.PI * u) * 0.45), pitch, roll: rollAt(ms), yaw: -0.5,
    stretch: 1 + warp * 2.2, flame: flameAt(ms), warp,
    visible: ms <= FLIGHT_MS + WARP_MS,
  };
}
