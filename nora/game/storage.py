"""Transacciones SQLite y recuperación conservadora de la partida."""
import json
from contextlib import contextmanager
import sqlite3
from .state import new_game
from .integrity import validate_game


class StorageError(Exception):
    pass


class Storage:
    def __init__(self, directory, now):
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.path = directory / 'station.sqlite3'
        try:
            with self.connect() as db:
                db.execute('PRAGMA secure_delete=ON')
                db.execute('CREATE TABLE IF NOT EXISTS current (id INTEGER PRIMARY KEY, value TEXT NOT NULL)')
                db.execute('CREATE TABLE IF NOT EXISTS metrics (value TEXT NOT NULL)')
                db.execute('CREATE TABLE IF NOT EXISTS consumption (id INTEGER PRIMARY KEY, tokens INTEGER NOT NULL)')
                db.execute('INSERT OR IGNORE INTO consumption VALUES (1, 0)')
                row = db.execute('SELECT value FROM current WHERE id=1').fetchone()
                game = json.loads(row[0]) if row else new_game(now)
                self.validate(game)
                self.save(game, db)
            self.path.chmod(0o600)
        except (sqlite3.Error, ValueError, KeyError, TypeError) as error:
            raise StorageError('Almacenamiento inválido. No se inició una partida nueva. Consulte docs/FACILITADOR.md.') from error

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path)
        try:
            db.execute('PRAGMA secure_delete=ON')
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def validate(game):
        validate_game(game, new_game(0).keys())

    def load(self):
        with self.connect() as db:
            return json.loads(db.execute('SELECT value FROM current WHERE id=1').fetchone()[0])

    def save(self, game, db=None):
        if db is None:
            with self.connect() as connection:
                self.save(game, connection)
        else:
            db.execute('INSERT OR REPLACE INTO current VALUES (1, ?)', (json.dumps(game, ensure_ascii=False),))

    def tokens(self):
        with self.connect() as db:
            return db.execute('SELECT tokens FROM consumption WHERE id=1').fetchone()[0]

    def add_tokens(self, count):
        with self.connect() as db:
            db.execute('UPDATE consumption SET tokens=tokens+? WHERE id=1', (count,))

    def reset(self, old, fresh, metric):
        with self.connect() as db:
            db.execute('INSERT INTO metrics VALUES (?)', (json.dumps(metric),))
            self.save(fresh, db)

    def metrics(self):
        with self.connect() as db:
            return [json.loads(row[0]) for row in db.execute('SELECT value FROM metrics')]
