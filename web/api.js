export class ApiError extends Error {
  constructor(message, status = 0) { super(message); this.status = status; }
}
export async function api(path, data) {
  let response;
  try {
    response = await fetch(path, { method: data ? 'POST' : 'GET', cache: 'no-store',
      headers: data ? { 'Content-Type': 'application/json' } : {},
      body: data ? JSON.stringify(data) : undefined, signal: AbortSignal.timeout(22000) });
  } catch { throw new ApiError('No hay comunicación con la estación. Avisen al facilitador y comprueben el servidor local.'); }
  const result = await response.json();
  if (!response.ok) throw new ApiError(result.error || 'No se pudo completar la solicitud.', response.status);
  return result;
}
export function showError(element, message = '') { element.textContent = message; element.hidden = !message; }
