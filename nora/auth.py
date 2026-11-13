"""Sesiones privadas en memoria, expiración y límite de intentos de acceso."""
import hashlib
import hmac
import secrets
import threading
import time
from http.cookies import SimpleCookie
from .game.errors import GameError


class Auth:
    def __init__(self, password, clock=time.time):
        self.clock = clock
        self.salt = secrets.token_bytes(16)
        self.enabled = len(password) >= 16
        self.digest = self.hash(password)
        self.sessions, self.attempts = {}, []
        self.lock = threading.Lock()

    def hash(self, password):
        return hashlib.scrypt(password.encode(), salt=self.salt, n=16384, r=8, p=1)

    def login(self, password):
        with self.lock:
            now = self.clock()
            self.attempts = [t for t in self.attempts if now - t < 60]
            if len(self.attempts) >= 5:
                raise GameError('Demasiados intentos. Espere un minuto.', 429)
            self.attempts.append(now)
            if not self.enabled:
                raise GameError('Configure FACILITATOR_PASSWORD con al menos 16 caracteres en el servidor.', 503)
            if not isinstance(password, str) or len(password) > 256 or not hmac.compare_digest(self.hash(password), self.digest):
                raise GameError('Credencial incorrecta.', 401)
            token = secrets.token_urlsafe(32)
            self.sessions = {key: expiry for key, expiry in self.sessions.items() if expiry > now}
            self.sessions[token] = now + 12 * 3600
            return token

    @staticmethod
    def token(header):
        cookie = SimpleCookie()
        try:
            cookie.load(header or '')
            return cookie['nora_facilitator'].value if 'nora_facilitator' in cookie else ''
        except Exception:
            return ''

    def require(self, header):
        token = self.token(header)
        with self.lock:
            if self.sessions.get(token, 0) <= self.clock():
                raise GameError('Acceso privado: inicie sesión como facilitador.', 401)
        return token

    def logout(self, header):
        with self.lock:
            self.sessions.pop(self.token(header), None)
