import tempfile
from pathlib import Path
from nora.config import Config
from nora.conversation.provider import local_interpret
from nora.game.station import Station
from nora.game.turns import turn


class Clock:
    def __init__(self): self.now = 1800000000
    def __call__(self): return self.now
    def advance(self, seconds): self.now += seconds


class FakeProvider:
    def interpret(self, game, text):
        return local_interpret(text), {'input_tokens': 10, 'output_tokens': 5}


def setup_station(test, provider=None, **config):
    directory = tempfile.TemporaryDirectory()
    test.addCleanup(directory.cleanup)
    clock = Clock()
    station = Station(Config(Path(directory.name), password='test-password-private-2026', **config), provider or FakeProvider(), clock)
    return station, clock


def start(station, local=True):
    id = station.game['id']
    if local: station.control(id, 'mode', 'local')
    station.control(id, 'start')
    return id


def chat(station, text, id=None):
    return turn(station, station.game['id'], id or 'msg-' + str(station.game['turns']), text)
