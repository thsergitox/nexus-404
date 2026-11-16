"""Turnos idempotentes; la llamada de red queda fuera del bloqueo del juego."""
import copy
import hashlib
import re
from .content import ACTIVE, REPLIES
from .errors import GameError
from .state import can_play, pause
from ..conversation.intents import authorize_intent
from ..conversation.provider import ProviderError, local_interpret, validate_output
from ..conversation.replies import reply


def validate_message(text, message_id):
    if not isinstance(text, str) or not text.strip():
        raise GameError('Escriban una solicitud antes de enviar.', 400)
    if len(text) > 800:
        raise GameError('El mensaje admite hasta 800 caracteres.', 400)
    if not isinstance(message_id, str) or not re.fullmatch(r'[a-zA-Z0-9-]{1,80}', message_id):
        raise GameError('Identificador de mensaje inválido.', 400)


def request_help(station, game_id):
    with station.lock:
        station.sync()
        station.require_game(game_id)
        if not can_play(station.game):
            raise GameError('El juego está detenido. Avisen al facilitador.')
        station.game['help_pending'] = True
        station.storage.save(station.game)
        return station.view()


def commit_intent(game, intent):
    if intent == 'PEDIR_AYUDA':
        game['help_pending'] = True
    if intent == 'ACTIVAR_MANTENIMIENTO' and game['phase'] == 'EN_CURSO':
        game['phase'] = 'MANTENIMIENTO'
    if intent == 'SOLICITUD_COMPLETA' or (intent == 'PEDIR_REPORTE' and game['phase'] in {'MANTENIMIENTO', 'REGISTRO_LIBERADO'}):
        game['phase'] = 'REGISTRO_LIBERADO'
        return 'LIBERAR'
    return intent


def account_usage(station, usage, same_game):
    counts = {key: max(0, int(usage.get(key, 0))) for key in ('input_tokens', 'output_tokens')}
    station.storage.add_tokens(sum(counts.values()))
    if same_game:
        for key, count in counts.items():
            station.game['usage'][key] += count


def turn(station, game_id, message_id, text):
    validate_message(text, message_id)
    digest = hashlib.sha256(text.encode()).hexdigest()
    with station.lock:
        station.sync()
        station.require_game(game_id)
        game = station.game
        if message_id in game['receipts']:
            if game['receipts'][message_id] != digest:
                raise GameError('Ese identificador ya corresponde a otro mensaje.')
            return station.view()
        if not can_play(game):
            raise GameError('El juego está detenido. Avisen al facilitador.')
        if station.pending is not None:
            raise GameError('NORA está respondiendo. Esperen antes de enviar otra solicitud.')
        if game['turns'] >= 250:
            raise GameError('Se alcanzó el límite de turnos. Avisen al facilitador.')
        if game['mode'] == 'generative' and station.config.token_limit and station.storage.tokens() >= station.config.token_limit:
            game.update(mode='local', technical='token_limit')
            pause(game, station.clock())
            station.storage.save(game)
            return station.view()
        ticket = (game_id, message_id, station.generation)
        station.pending = ticket
        snapshot = copy.deepcopy(game)
        if snapshot['mode'] == 'generative':
            game['usage']['requests'] += 1
    result, error, usage = None, None, {}
    try:
        if snapshot['mode'] == 'local':
            result = local_interpret(text)
        else:
            result, usage = station.provider.interpret(snapshot, text)
        validate_output(result, snapshot['hints'])
    except ProviderError as failure:
        error, usage = failure.reason, failure.usage
    except Exception:
        error = 'service_error'
    with station.lock:
        station.sync()
        same_game = station.game['id'] == game_id
        account_usage(station, usage, same_game)
        if station.pending == ticket:
            station.pending = None
        if not same_game or station.generation != ticket[2] or not can_play(station.game):
            station.storage.save(station.game)
            return station.view()
        game = station.game
        game['receipts'][message_id] = digest
        game['turns'] += 1
        game['messages'].append(dict(role='user', text=text.strip(), id=message_id))
        if error:
            game.update(technical=error, errors=game['errors'] + 1)
            pause(game, station.clock())
            game['messages'].append(dict(role='system', text=REPLIES['ERROR'], id=message_id + '-error'))
        else:
            intent = authorize_intent(text, result['intencion'], snapshot)
            event = commit_intent(game, intent)
            response = REPLIES['LIBERAR'] if event == 'LIBERAR' else reply(intent, result, text, game, station.config.strict)
            game['messages'].append(dict(role='system' if event == 'LIBERAR' else 'assistant',
                                         text=response, id=message_id + '-reply', card=event == 'LIBERAR'))
        game['revision'] += 1
        station.storage.save(game)
        return station.view()
