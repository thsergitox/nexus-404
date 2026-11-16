"""HTTP limitado a loopback y archivos públicos enumerados explícitamente."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from .auth import Auth
from .config import ROOT
from .game.content import HINTS
from .game.briefing import NOTES
from .game.errors import GameError
from .game.turns import turn, request_help
from .game.validation import validate_code

FILES = {
    '/': ('index.html', 'text/html'), '/facilitador': ('facilitator.html', 'text/html'),
    '/app.js': ('app.js', 'text/javascript'), '/api.js': ('api.js', 'text/javascript'),
    '/render.js': ('render.js', 'text/javascript'), '/panels.js': ('panels.js', 'text/javascript'),
    '/facilitator.js': ('facilitator.js', 'text/javascript'),
    '/styles/base.css': ('styles/base.css', 'text/css'),
    '/styles/player.css': ('styles/player.css', 'text/css'),
    '/styles/facilitator.css': ('styles/facilitator.css', 'text/css'),
    '/briefing.js': ('briefing.js', 'text/javascript'),
    '/print-notes.css': ('../materials/print-notes.css', 'text/css'),
    '/notas-imprimibles': ('../materials/notas.html', 'text/html'),
    '/mark.svg': ('mark.svg', 'image/svg+xml'),
}
COOKIE = 'nora_facilitator={}; HttpOnly; SameSite=Strict; Path=/api/admin; Max-Age={}'


def make_server(station, port=None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass  # No almacenar texto libre, credenciales ni URLs introducidas por visitantes.

        def check_origin(self):
            allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            host = self.headers.get('Host', '')
            if host not in allowed:
                raise GameError('Host no permitido. Use localhost.', 403)
            origin = self.headers.get('Origin')
            if origin and origin not in {f'http://{h}' for h in allowed}:
                raise GameError('Origen no permitido.', 403)

        def send(self, value, status=200, mime='application/json', cookie=None):
            body = json.dumps(value, ensure_ascii=False).encode() if mime == 'application/json' else value
            self.send_response(status)
            self.send_header('Content-Type', mime + ('; charset=utf-8' if mime.startswith('text/') or mime == 'application/json' else ''))
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
            if cookie:
                self.send_header('Set-Cookie', cookie)
            self.end_headers()
            self.wfile.write(body)

        def body(self):
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                raise GameError('Se requiere JSON.', 415)
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 8192:
                    raise ValueError('length')
                self.connection.settimeout(5)
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError('object')
                return data
            except (ValueError, OSError):
                raise GameError('Solicitud inválida o demasiado grande.', 400)

        def do_GET(self):
            try:
                self.check_origin()
                path = urlsplit(self.path).path
                if path == '/api/briefing':
                    return self.send({'notes': NOTES})
                if path == '/api/state':
                    return self.send(station.view())
                if path == '/api/admin/state':
                    self.server.auth.require(self.headers.get('Cookie'))
                    return self.send(dict(**station.private_view(), hint_catalog=HINTS))
                if path in FILES:
                    file, mime = FILES[path]
                    return self.send((ROOT / 'web' / file).read_bytes(), mime=mime)
                raise GameError('Recurso no disponible.', 404)
            except GameError as error:
                self.send({'error': error.message}, error.status)
            except (BrokenPipeError, ConnectionResetError):
                pass
            except Exception:
                self.send({'error': 'Error local. Avisen al facilitador; el progreso se conserva.'}, 500)

        def do_POST(self):
            try:
                self.check_origin()
                path = urlsplit(self.path).path
                data = self.body()
                if path == '/api/admin/login':
                    token = self.server.auth.login(data.get('password'))
                    return self.send({'ok': True}, cookie=COOKIE.format(token, 43200))
                if path.startswith('/api/admin/'):
                    self.server.auth.require(self.headers.get('Cookie'))
                    if path == '/api/admin/logout':
                        self.server.auth.logout(self.headers.get('Cookie'))
                        return self.send({'ok': True}, cookie=COOKIE.format('', 0))
                    if path == '/api/admin/control':
                        return self.send(station.control(data.get('game_id'), data.get('action'), data.get('value')))
                if path == '/api/chat':
                    return self.send(turn(station, data.get('game_id'), data.get('message_id'), data.get('text')))
                if path == '/api/help':
                    return self.send(request_help(station, data.get('game_id')))
                if path == '/api/validate':
                    return self.send(validate_code(station, data.get('game_id'), data.get('code')))
                raise GameError('Recurso no disponible.', 404)
            except GameError as error:
                self.send({'error': error.message}, error.status)
            except (BrokenPipeError, ConnectionResetError):
                pass
            except Exception:
                self.send({'error': 'Error local. Avisen al facilitador; el progreso se conserva.'}, 500)

    server = ThreadingHTTPServer(('127.0.0.1', station.config.port if port is None else port), Handler)
    server.auth = Auth(station.config.password)
    return server
