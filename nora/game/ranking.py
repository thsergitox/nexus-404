"""Mejores tiempos del evento: el servidor mide el tiempo y el grupo solo elige su nombre."""
import re
from .errors import GameError

NAME_MAX = 24
TOP_SIZE = 10
NAME_PATTERN = re.compile(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ .,'!¡?¿&-]+")
COLUMNS = 'id, name, seconds, hints, assisted, finished'


def clean_name(value):
    if not isinstance(value, str):
        raise GameError('Escriban un nombre para la tripulación.', 400)
    name = ' '.join(value.split())
    if not name:
        raise GameError('Escriban un nombre para la tripulación.', 400)
    if len(name) > NAME_MAX:
        raise GameError(f'El nombre admite hasta {NAME_MAX} caracteres.', 400)
    if not NAME_PATTERN.fullmatch(name):
        raise GameError('Usen solo letras, números, espacios y signos básicos.', 400)
    return name


def as_entry(row):
    return dict(id=row[0], name=row[1], seconds=row[2], hints=row[3], assisted=bool(row[4]), finished=row[5])


class Ranking:
    def __init__(self, storage):
        self.storage = storage
        with storage.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS ranking (id INTEGER PRIMARY KEY AUTOINCREMENT, game_id TEXT UNIQUE NOT NULL, '
                       'name TEXT, seconds INTEGER NOT NULL, hints INTEGER NOT NULL, assisted INTEGER NOT NULL, finished REAL NOT NULL)')

    def record(self, game_id, seconds, hints, assisted, finished):
        with self.storage.connect() as db:
            db.execute('INSERT OR IGNORE INTO ranking (game_id, seconds, hints, assisted, finished) VALUES (?, ?, ?, ?, ?)',
                       (game_id, seconds, hints, int(assisted), finished))

    def named(self, game_id):
        with self.storage.connect() as db:
            row = db.execute('SELECT name FROM ranking WHERE game_id=?', (game_id,)).fetchone()
        return None if row is None else row[0] is not None

    def rename(self, game_id, name):
        with self.storage.connect() as db:
            changed = db.execute('UPDATE ranking SET name=? WHERE game_id=? AND name IS NULL', (clean_name(name), game_id)).rowcount
        if not changed:
            raise GameError('Esta tripulación ya está registrada en el ranking.', 409)

    def entries(self):
        with self.storage.connect() as db:
            return [as_entry(row) for row in db.execute(f'SELECT {COLUMNS} FROM ranking ORDER BY seconds, finished')]

    def top(self):
        return self.entries()[:TOP_SIZE]

    def delete(self, ids):
        if not isinstance(ids, list) or not ids or any(type(i) is not int for i in ids):
            raise GameError('Seleccionen al menos un tiempo para eliminar.', 400)
        with self.storage.connect() as db:
            db.executemany('DELETE FROM ranking WHERE id=?', [(i,) for i in ids])

    def clear(self):
        with self.storage.connect() as db:
            db.execute('DELETE FROM ranking')
