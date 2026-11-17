import { timeText } from './render.js';

export const crewName = entry => entry.name || 'Tripulación sin nombre';
export const crewTime = entry => timeText(entry.seconds);

export function supportText(entry) {
  const hints = entry.hints === 1 ? '1 ayuda' : `${entry.hints} ayudas`;
  return entry.assisted ? `${hints} · con asistencia` : hints;
}
