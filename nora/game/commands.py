"""Acciones administrativas; solo se invocan tras autenticación HTTP."""
from .content import ACTIVE, HINTS, REPLIES
from .errors import GameError
from .state import pause, resume


def command(game, action, value, now):
    phase = game['phase']
    if action == 'start' and phase == 'PREPARADA':
        game.update(phase='EN_CURSO', started=now, deadline=now + game['remaining'])
    elif action == 'pause' and phase in ACTIVE:
        pause(game, now)
    elif action == 'resume' and phase in ACTIVE and game['paused']:
        resume(game, now)
    elif action == 'extend' and phase in ACTIVE | {'AGOTADA'}:
        if type(value) is not int or not 30 <= value <= 900:
            raise GameError('La extensión debe ser de 30 a 900 segundos.', 400)
        was_expired = phase == 'AGOTADA'
        was_paused = game['paused']
        pause(game, now)
        game['remaining'] += value
        if was_expired:
            game['phase'] = game['previous']
            game['previous'] = None
            resume(game, now)
        elif not was_paused:
            resume(game, now)
    elif action == 'mode' and value in {'local', 'generative'}:
        game['mode'] = value
    elif action == 'hint' and phase in ACTIVE:
        if value not in HINTS:
            raise GameError('Ayuda desconocida.', 400)
        if value.startswith('B') and phase != 'REGISTRO_LIBERADO':
            raise GameError('El apoyo binario requiere el registro recuperado.')
        if value not in game['hints']:
            game['hints'].append(value)
            game['help_pending'] = False
    elif action == 'release' and phase in ACTIVE:
        game.update(phase='REGISTRO_LIBERADO', assisted=True)
        if not any(m['id'] == 'assistance' for m in game['messages']):
            game['messages'].append(dict(role='system', text=REPLIES['LIBERAR'], id='assistance', card=True))
    else:
        raise GameError('Esta acción no está disponible en el estado actual.')
    game['revision'] += 1
