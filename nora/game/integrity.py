"""Comprobación del almacenamiento antes de aceptar una partida recuperada."""
import math
import uuid
from .content import ACTIVE, HINTS


def number(value):
    return type(value) in {int, float} and math.isfinite(value) and value >= 0


def validate_game(game, required):
    if not isinstance(game, dict) or not required <= game.keys():
        raise ValueError('estructura')
    if not isinstance(game['id'], str):
        raise ValueError('identificador')
    uuid.UUID(game['id'])
    phase = game['phase']
    if phase not in ACTIVE | {'PREPARADA', 'AGOTADA', 'RESUELTA'}:
        raise ValueError('fase')
    if game['previous'] is not None and game['previous'] not in ACTIVE:
        raise ValueError('fase previa')
    if phase == 'AGOTADA' and game['previous'] is None:
        raise ValueError('recuperación')
    if game['mode'] not in {'generative', 'local'}:
        raise ValueError('modo')
    for field in ('paused', 'help_pending', 'assisted'):
        if type(game[field]) is not bool:
            raise ValueError(field)
    for field in ('remaining', 'revision', 'turns', 'errors'):
        if not number(game[field]):
            raise ValueError(field)
    for field in ('deadline', 'started'):
        if game[field] is not None and not number(game[field]):
            raise ValueError(field)
    running = phase in ACTIVE and not game['paused']
    if running != (game['deadline'] is not None):
        raise ValueError('reloj')
    hints = game['hints']
    if not isinstance(hints, list) or any(h not in HINTS for h in hints) or len(hints) != len(set(hints)):
        raise ValueError('ayudas')
    if not isinstance(game['receipts'], dict):
        raise ValueError('idempotencia')
    if not isinstance(game['usage'], dict) or not {'requests', 'input_tokens', 'output_tokens'} <= game['usage'].keys():
        raise ValueError('consumo')
    if any(not number(v) for v in game['usage'].values()):
        raise ValueError('consumo')
    if not isinstance(game['messages'], list) or not game['messages']:
        raise ValueError('historial')
    for message in game['messages']:
        if not isinstance(message, dict) or message.get('role') not in {'user', 'assistant', 'system'}:
            raise ValueError('mensaje')
        if not isinstance(message.get('text'), str) or not isinstance(message.get('id'), str):
            raise ValueError('contenido')
