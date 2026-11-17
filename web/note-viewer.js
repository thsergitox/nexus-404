const EXPAND = { duration: 420, easing: 'cubic-bezier(.2,.9,.25,1)' };
const COLLAPSE = { duration: 300, easing: 'cubic-bezier(.6,0,.8,.4)' };

function originTransform(from, to) {
  const dx = from.left + from.width / 2 - (to.left + to.width / 2);
  const dy = from.top + from.height / 2 - (to.top + to.height / 2);
  return `translate(${dx}px, ${dy}px) scale(${from.width / to.width}, ${from.height / to.height})`;
}

function prefersStillness() {
  return matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function fill(dialog, note) {
  dialog.querySelector('#note-dialog-label').textContent = `Fragmento ${note.id} · Expediente de la tripulación`;
  dialog.querySelector('#note-dialog-title').textContent = note.title;
  dialog.querySelector('#note-dialog-text').textContent = note.text;
  dialog.querySelector('#note-dialog-author').textContent = note.author;
}

export function createNoteViewer(dialog) {
  const sheet = dialog.querySelector('.note-sheet');
  let origin = null;

  function morph(keyframes, timing) {
    if (prefersStillness() || !origin?.isConnected) return Promise.resolve();
    return sheet.animate(keyframes, timing).finished.catch(() => {});
  }

  async function close() {
    if (!dialog.open || dialog.classList.contains('closing')) return;
    dialog.classList.add('closing');
    const start = originTransform(origin.getBoundingClientRect(), sheet.getBoundingClientRect());
    await morph([{ transform: 'none', opacity: 1 }, { transform: start, opacity: .4 }], COLLAPSE);
    dialog.classList.remove('closing'); dialog.close();
    origin?.focus();
  }

  function open(note, card) {
    origin = card; fill(dialog, note);
    dialog.showModal();
    const start = originTransform(card.getBoundingClientRect(), sheet.getBoundingClientRect());
    morph([{ transform: start, opacity: .4 }, { transform: 'none', opacity: 1 }], EXPAND);
  }

  dialog.addEventListener('cancel', event => { event.preventDefault(); close(); });
  dialog.addEventListener('click', event => { if (event.target === dialog) close(); });
  dialog.querySelector('.note-close').addEventListener('click', close);
  return { open };
}
