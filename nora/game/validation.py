"""La única ruta de victoria oficial, autorizada por el estado del servidor."""
import hmac
import re
from .content import CODE, REPLIES
from .errors import GameError
from .state import can_play, remaining


def validate_code(station, game_id, code):
    with station.lock:
        station.sync()
        station.require_game(game_id)
        game = station.game
        if game['phase'] == 'RESUELTA':
            return station.view()
        if game['phase'] != 'REGISTRO_LIBERADO' or not can_play(game):
            raise GameError('La consola no está habilitada. Avisen al facilitador si el juego está detenido.')
        if not isinstance(code, str) or not re.fullmatch(r'[0-9]{4}', code.strip()):
            raise GameError('Escriban exactamente cuatro dígitos, sin espacios interiores.', 400)
        if not hmac.compare_digest(code.strip(), CODE):
            raise GameError('Código no válido. Revisen las equivalencias y el orden.', 422)
        game.update(remaining=remaining(game, station.clock()), deadline=None, phase='RESUELTA')
        game['messages'].append(dict(role='system', text=REPLIES['VICTORY'], id='victory'))
        game['revision'] += 1
        station.generation += 1
        station.storage.save(game)
        return station.view()
