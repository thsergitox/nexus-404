const COUNT = 380;
const DEPTH_FADE = 0.12;

function spawn(star, far = true) {
  star.x = (Math.random() - 0.5) * 2.4;
  star.y = (Math.random() - 0.5) * 1.6;
  star.z = far ? 1 : Math.random() * 0.95 + 0.05;
  star.hue = Math.random() < 0.12 ? 'warm' : 'cold';
  star.px = null;
  return star;
}

export function createStarfield() {
  const stars = Array.from({ length: COUNT }, () => spawn({}, false));

  function project(star, width, height, parallax) {
    const fov = Math.min(width, height) * 0.9;
    return { x: width / 2 + (star.x + parallax.x * (1 - star.z) * 0.06) / star.z * fov,
      y: height / 2 + (star.y + parallax.y * (1 - star.z) * 0.06) / star.z * fov };
  }

  function draw(context, width, height, { speed, delta, parallax, palette }) {
    const streak = speed > 0.25;
    context.lineCap = 'round';
    for (const star of stars) {
      star.z -= speed * delta;
      if (star.z <= 0.02) spawn(star);
      const point = project(star, width, height, parallax);
      if (point.x < -50 || point.x > width + 50 || point.y < -50 || point.y > height + 50) { spawn(star); continue; }
      const near = 1 - star.z;
      const alpha = Math.min(1, near / DEPTH_FADE) * (0.25 + near * 0.75);
      const size = 0.4 + near * 1.8;
      const color = star.hue === 'warm' ? palette.warm : palette.star;
      if (streak && star.px) {
        context.strokeStyle = `rgba(${color},${alpha})`; context.lineWidth = size;
        context.beginPath(); context.moveTo(star.px.x, star.px.y); context.lineTo(point.x, point.y); context.stroke();
      } else {
        context.fillStyle = `rgba(${color},${alpha})`;
        context.fillRect(point.x, point.y, size, size);
      }
      star.px = point;
    }
  }

  return { draw };
}
