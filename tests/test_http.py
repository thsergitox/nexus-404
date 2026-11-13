import http.client
import json
import threading
import unittest
from nora.http import make_server, FILES
from nora.config import ROOT
from tests.support import setup_station


class HttpSecurity(unittest.TestCase):
    def setUp(self):
        self.s, self.clock = setup_station(self)
        self.server = make_server(self.s, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True); self.thread.start()
        self.addCleanup(self.close)
    def close(self): self.server.shutdown(); self.server.server_close(); self.thread.join()
    def request(self, path, data=None, cookie='', extra=None):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        headers = {'Content-Type': 'application/json', 'Cookie': cookie, **(extra or {})}
        connection.request('POST' if data is not None else 'GET', path, json.dumps(data) if data is not None else None, headers)
        response = connection.getresponse(); body = response.read(); status = response.status; headers = dict(response.getheaders()); connection.close()
        return status, body, headers
    def login(self):
        status, body, headers = self.request('/api/admin/login', {'password': self.s.config.password})
        self.assertEqual(status, 200)
        return headers['Set-Cookie'].split(';')[0]

    def test_O19_auth_required_even_direct_endpoint(self):
        for path, data in [('/api/admin/state', None), ('/api/admin/control', {'game_id': self.s.game['id'], 'action': 'start'})]:
            self.assertEqual(self.request(path, data)[0], 401)
        cookie = self.login()
        self.assertEqual(self.request('/api/admin/control', {'game_id': self.s.game['id'], 'action': 'start'}, cookie)[0], 200)
        self.request('/api/admin/logout', {}, cookie)
        self.assertEqual(self.request('/api/admin/state', cookie=cookie)[0], 401)

    def test_O20_no_secrets_in_public_assets(self):
        for path in FILES:
            status, body, _ = self.request(path)
            self.assertEqual(status, 200)
            self.assertNotIn(b'5936', body)
            self.assertNotIn(self.s.config.password.encode(), body)
            self.assertNotIn(b'0101', body)
        for path in ['/.env', '/nora/game/content.py', '/../.env', '/data/station.sqlite3', '/tests/cases.json']:
            self.assertEqual(self.request(path)[0], 404)
        body = self.request('/api/state')[1]
        self.assertNotIn(b'5936', body); self.assertNotIn(b'0101', body)

    def test_origin_and_host_rebinding(self):
        self.assertEqual(self.request('/api/admin/login', {'password': self.s.config.password}, extra={'Origin': 'https://attacker.invalid'})[0], 403)
        self.assertEqual(self.request('/api/state', extra={'Host': 'attacker.invalid'})[0], 403)

    def test_login_throttle_and_cookie_flags(self):
        _, _, headers = self.request('/api/admin/login', {'password': self.s.config.password})
        self.assertIn('HttpOnly', headers['Set-Cookie']); self.assertIn('SameSite=Strict', headers['Set-Cookie'])
        for _ in range(4): self.assertEqual(self.request('/api/admin/login', {'password': 'incorrect'})[0], 401)
        self.assertEqual(self.request('/api/admin/login', {'password': 'incorrect'})[0], 429)
        self.clock.advance(61)

    def test_bad_json_not_500(self):
        self.assertEqual(self.request('/api/chat', [1,2])[0], 400)
        self.assertEqual(self.request('/api/chat', {'text':'hola'})[0], 400)
