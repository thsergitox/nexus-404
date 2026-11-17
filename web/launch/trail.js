const MAX_PARTICLES = 420;

export function createTrail() {
  const particles = [];

  function emit(x, y, angle, strength) {
    const count = Math.round(2 + strength * 4);
    for (let i = 0; i < count && particles.length < MAX_PARTICLES; i++) {
      const spread = angle + (Math.random() - 0.5) * 0.5;
      const speed = 40 + Math.random() * 90 * strength;
      particles.push({ x, y, vx: Math.cos(spread) * speed, vy: Math.sin(spread) * speed,
        life: 0, max: 0.5 + Math.random() * 0.7, size: 1.5 + Math.random() * 3 * strength });
    }
  }

  function update(seconds) {
    for (let i = particles.length - 1; i >= 0; i--) {
      const particle = particles[i];
      particle.life += seconds;
      if (particle.life >= particle.max) { particles.splice(i, 1); continue; }
      particle.x += particle.vx * seconds; particle.y += particle.vy * seconds;
      particle.vx *= 0.96; particle.vy *= 0.96;
    }
  }

  function draw(context) {
    context.save(); context.globalCompositeOperation = 'lighter';
    for (const particle of particles) {
      const age = particle.life / particle.max;
      context.fillStyle = age < 0.35 ? `rgba(198,243,107,${0.8 * (1 - age)})` : `rgba(110,242,255,${0.6 * (1 - age)})`;
      context.beginPath(); context.arc(particle.x, particle.y, particle.size * (1 - age * 0.6), 0, Math.PI * 2); context.fill();
    }
    context.restore();
  }

  return { emit, update, draw };
}
