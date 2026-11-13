"""Fachada transaccional de la única estación activa."""
import threading
import time
from .commands import command
from .errors import GameError
from .state import new_game, public_state, synchronize
from .storage import Storage
from ..conversation.prompt import VERSION


class Station:
    def __init__(self, config, provider, clock=time.time):
        self.config, self.provider, self.clock = config, provider, clock
        self.lock = threading.RLock()
        self.storage = Storage(config.data_dir, clock())
        self.game = self.storage.load()
        self.pending = None
        self.generation = 0

    def sync(self):
        synchronize(self.game, self.clock())
        self.storage.save(self.game)

    def view(self):
        with self.lock:
            self.sync()
            return public_state(self.game, self.clock(), self.pending is not None)

    def private_view(self):
        with self.lock:
            result = self.view()
            result.update(technical_reason=self.game['technical'], usage=self.game['usage'],
                          event_tokens=self.storage.tokens(), token_limit=self.config.token_limit,
                          api_configured=bool(self.config.api_key), model=self.config.model,
                          prompt_version=VERSION, assisted=self.game['assisted'],
                          strict_catalog=self.config.strict, metrics=self.storage.metrics())
            return result

    def require_game(self, game_id):
        if game_id != self.game['id']:
            raise GameError('La partida cambió. Se ha actualizado la consola.')

    def control(self, game_id, action, value=None):
        with self.lock:
            self.sync()
            self.require_game(game_id)
            if action == 'reset':
                if value != game_id:
                    raise GameError('Confirme el reinicio de esta partida.', 400)
                metric = dict(result=self.game['phase'], turns=self.game['turns'],
                              hints=self.game['hints'], assisted=self.game['assisted'],
                              errors=self.game['errors'], usage=self.game['usage'],
                              model=self.config.model, prompt_version=VERSION,
                              duration=0 if self.game['started'] is None else round(self.clock() - self.game['started']))
                fresh = new_game(self.clock())
                self.storage.reset(self.game, fresh, metric)
                self.game = fresh
                self.pending = None
            else:
                command(self.game, action, value, self.clock())
                self.storage.save(self.game)
            if action not in {'hint'}:
                self.generation += 1
            return self.private_view()
