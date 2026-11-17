const BOOT_MS = 3200;
const SEEN_KEY = 'nexus-boot-seen';

function alreadySeen() {
  try { return sessionStorage.getItem(SEEN_KEY) === '1'; } catch { return false; }
}

function remember() {
  try { sessionStorage.setItem(SEEN_KEY, '1'); } catch { /* almacenamiento bloqueado: el arranque se repetirá */ }
}

function dismiss(boot) {
  if (boot.classList.contains('leaving')) return;
  boot.classList.add('leaving'); remember();
  boot.addEventListener('animationend', () => boot.remove(), { once: true });
  setTimeout(() => boot.remove(), 900);
}

const boot = document.querySelector('#boot');
if (boot) {
  if (alreadySeen() || matchMedia('(prefers-reduced-motion: reduce)').matches) boot.remove();
  else {
    const skip = () => dismiss(boot);
    setTimeout(skip, BOOT_MS);
    boot.addEventListener('click', skip);
    window.addEventListener('keydown', skip, { once: true });
  }
}
