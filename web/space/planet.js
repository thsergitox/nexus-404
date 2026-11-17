const LATITUDES = 9;
const LONGITUDES = 18;
const SAMPLES = 56;
const TILT = 0.42;
const RING_RADIUS = 1.55;

function rotate([x, y, z], spin) {
  const cosY = Math.cos(spin), sinY = Math.sin(spin);
  const rx = x * cosY + z * sinY, rz = -x * sinY + z * cosY;
  const cosX = Math.cos(TILT), sinX = Math.sin(TILT);
  return [rx, y * cosX - rz * sinX, y * sinX + rz * cosX];
}

function sphereLines() {
  const lines = [];
  for (let i = 1; i < LATITUDES; i++) {
    const phi = (i / LATITUDES) * Math.PI - Math.PI / 2;
    lines.push(Array.from({ length: SAMPLES + 1 }, (_, s) => {
      const theta = (s / SAMPLES) * Math.PI * 2;
      return [Math.cos(phi) * Math.cos(theta), Math.sin(phi), Math.cos(phi) * Math.sin(theta)];
    }));
  }
  for (let j = 0; j < LONGITUDES; j++) {
    const theta = (j / LONGITUDES) * Math.PI * 2;
    lines.push(Array.from({ length: SAMPLES + 1 }, (_, s) => {
      const phi = (s / SAMPLES) * Math.PI - Math.PI / 2;
      return [Math.cos(phi) * Math.cos(theta), Math.sin(phi), Math.cos(phi) * Math.sin(theta)];
    }));
  }
  return lines;
}

const ringLine = Array.from({ length: SAMPLES * 2 + 1 }, (_, s) => {
  const theta = (s / (SAMPLES * 2)) * Math.PI * 2;
  return [Math.cos(theta) * RING_RADIUS, 0, Math.sin(theta) * RING_RADIUS];
});

function strokeByDepth(context, points, center, radius, palette, { front, back, occlude }) {
  const frontPath = new Path2D(), backPath = new Path2D();
  for (let i = 1; i < points.length; i++) {
    const [a, b] = [points[i - 1], points[i]];
    const depth = (a[2] + b[2]) / 2;
    const hidden = occlude && depth > 0 && Math.hypot(b[0], b[1]) < 1;
    if (hidden) continue;
    const path = depth <= 0 ? frontPath : backPath;
    path.moveTo(center.x + a[0] * radius, center.y + a[1] * radius);
    path.lineTo(center.x + b[0] * radius, center.y + b[1] * radius);
  }
  context.strokeStyle = `rgba(${palette.line},${back})`; context.stroke(backPath);
  context.strokeStyle = `rgba(${palette.line},${front})`; context.stroke(frontPath);
}

export function createPlanet() {
  const lines = sphereLines();

  function draw(context, width, height, { time, palette }) {
    const radius = Math.min(width, height) * (width < 760 ? 0.36 : 0.44);
    const center = { x: width * (width < 760 ? 0.82 : 0.88), y: height * 0.82 };
    const spin = time * 0.00006;
    const glow = context.createRadialGradient(center.x, center.y, radius * 0.7, center.x, center.y, radius * 1.45);
    glow.addColorStop(0, `rgba(${palette.line},0.22)`); glow.addColorStop(1, `rgba(${palette.line},0)`);
    context.fillStyle = glow; context.beginPath(); context.arc(center.x, center.y, radius * 1.45, 0, Math.PI * 2); context.fill();

    const ring = ringLine.map(point => rotate(point, spin * 0.6));
    context.lineWidth = 1;
    strokeByDepth(context, ring, center, radius, palette, { front: 0, back: 0.35, occlude: true });

    const body = context.createRadialGradient(center.x - radius * 0.35, center.y - radius * 0.4, radius * 0.1, center.x, center.y, radius);
    body.addColorStop(0, palette.surfaceLight); body.addColorStop(1, palette.surfaceDark);
    context.fillStyle = body; context.beginPath(); context.arc(center.x, center.y, radius, 0, Math.PI * 2); context.fill();

    lines.forEach(line => strokeByDepth(context, line.map(point => rotate(point, spin)), center, radius, palette, { front: 0.42, back: 0.07 }));
    strokeByDepth(context, ring, center, radius, palette, { front: 0.6, back: 0, occlude: false });

    const orbit = time * 0.00018;
    const station = rotate([Math.cos(orbit) * RING_RADIUS, 0, Math.sin(orbit) * RING_RADIUS], spin * 0.6);
    if (station[2] <= 0 || Math.hypot(station[0], station[1]) >= 1) {
      const x = center.x + station[0] * radius, y = center.y + station[1] * radius;
      context.fillStyle = `rgba(${palette.beacon},0.25)`; context.beginPath(); context.arc(x, y, 9, 0, Math.PI * 2); context.fill();
      context.fillStyle = `rgba(${palette.beacon},1)`; context.beginPath(); context.arc(x, y, 3, 0, Math.PI * 2); context.fill();
    }
  }

  return { draw };
}
