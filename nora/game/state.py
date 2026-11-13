"""Reloj y proyección pública; ningún reloj del navegador autoriza acciones."""
import math
import uuid
from .content import BLOCKS, HINTS, INTRO, ACTIVE


def new_game(now):
    return dict(id=str(uuid.uuid4()), phase='PREPARADA', previous=None, paused=False,
                mode='generative', remaining=900, deadline=None, hints=[], help_pending=False,
                messages=[dict(role='assistant', text=INTRO, id='intro')], receipts={},
                technical=None, revision=0, started=None, turns=0, errors=0,
                assisted=False, usage=dict(requests=0, input_tokens=0, output_tokens=0))


def remaining(game, now):
    if game['deadline'] is not None:
        return max(0, game['deadline'] - now)
    return game['remaining']


def synchronize(game, now):
    if game['phase'] in ACTIVE and not game['paused'] and remaining(game, now) <= 0:
        game.update(previous=game['phase'], phase='AGOTADA', remaining=0, deadline=None)
        game['revision'] += 1


def pause(game, now):
    game.update(remaining=remaining(game, now), deadline=None, paused=True)


def resume(game, now):
    game.update(deadline=now + game['remaining'], paused=False, technical=None)


def can_play(game):
    return game['phase'] in ACTIVE and not game['paused']


def revealed(game):
    return game['phase'] in {'REGISTRO_LIBERADO', 'RESUELTA'} or game['previous'] == 'REGISTRO_LIBERADO'


def public_state(game, now, pending=False):
    return dict(id=game['id'], phase=game['phase'], paused=game['paused'],
                remaining=math.ceil(remaining(game, now)), mode=game['mode'],
                hints=[dict(id=h, text=HINTS[h]) for h in game['hints']],
                help_pending=game['help_pending'], messages=game['messages'],
                blocks=BLOCKS if revealed(game) else None,
                technical=bool(game['technical']), revision=game['revision'],
                pending=pending, playable=can_play(game))
