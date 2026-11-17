import http.client
import json
import threading
import unittest
from nora.game.content import CODE
from nora.game.errors import GameError
from nora.game.validation import validate_code
from nora.http import make_server
from tests.support import setup_station, start


def win(station, clock, seconds):
    start(station)
    clock.advance(seconds)
    station.control(station.game['id'], 'release')
    return validate_code(station, station.game['id'], CODE)


def next_group(station):
    station.control(station.game['id'], 'reset', station.game['id'])


class RankingRules(unittest.TestCase):
    def setUp(self):
        self.s, self.clock = setup_station(self)

    def test_victory_records_elapsed_time_without_name(self):
        view = win(self.s, self.clock, 312)
        self.assertIs(view['crew_named'], False)
        [entry] = self.s.ranking.entries()
        self.assertEqual((entry['seconds'], entry['name'], entry['assisted']), (312, None, True))

    def test_crew_names_itself_once(self):
        win(self.s, self.clock, 200)
        game_id = self.s.game['id']
        self.s.name_crew(game_id, '  Los   Halcones ')
        self.assertEqual(self.s.ranking.entries()[0]['name'], 'Los Halcones')
        self.assertIs(self.s.view()['crew_named'], True)
        with self.assertRaises(GameError):
            self.s.name_crew(game_id, 'Otro nombre')

    def test_name_requires_victory_and_valid_text(self):
        start(self.s)
        with self.assertRaises(GameError):
            self.s.name_crew(self.s.game['id'], 'Antes de ganar')
        next_group(self.s); win(self.s, self.clock, 100)
        for bad in ['', '   ', 'x' * 25, '<script>', 123]:
            with self.assertRaises(GameError):
                self.s.name_crew(self.s.game['id'], bad)

    def test_top_orders_fastest_first(self):
        for seconds in (500, 120, 300):
            win(self.s, self.clock, seconds); next_group(self.s)
        self.assertEqual([e['seconds'] for e in self.s.ranking.top()], [120, 300, 500])

    def test_delete_selected_and_clear(self):
        for seconds in (100, 200, 300):
            win(self.s, self.clock, seconds); next_group(self.s)
        ids = [e['id'] for e in self.s.ranking.entries()]
        self.s.ranking.delete(ids[:2])
        self.assertEqual([e['seconds'] for e in self.s.ranking.entries()], [300])
        self.s.ranking.clear()
        self.assertEqual(self.s.ranking.entries(), [])

    def test_replayed_victory_does_not_duplicate(self):
        win(self.s, self.clock, 150)
        validate_code(self.s, self.s.game['id'], CODE)
        self.assertEqual(len(self.s.ranking.entries()), 1)


class RankingHttp(unittest.TestCase):
    def setUp(self):
        self.s, self.clock = setup_station(self)
        self.server = make_server(self.s, 0)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True); thread.start()
        self.addCleanup(lambda: (self.server.shutdown(), self.server.server_close(), thread.join()))

    def request(self, path, data=None, cookie=''):
        connection = http.client.HTTPConnection('127.0.0.1', self.server.server_port)
        connection.request('POST' if data is not None else 'GET', path, json.dumps(data) if data is not None else None,
                           {'Content-Type': 'application/json', 'Cookie': cookie})
        response = connection.getresponse(); body = json.loads(response.read() or 'null')
        headers = dict(response.getheaders()); connection.close()
        return response.status, body, headers

    def test_public_top_hides_ids_and_admin_can_delete(self):
        win(self.s, self.clock, 240)
        self.request('/api/ranking/name', {'game_id': self.s.game['id'], 'name': 'Nebulosa'})
        status, body, _ = self.request('/api/ranking')
        self.assertEqual(status, 200)
        self.assertEqual(body['entries'][0]['name'], 'Nebulosa')
        self.assertNotIn('id', body['entries'][0])
        self.assertEqual(self.request('/api/admin/ranking/delete', {'ids': [1]})[0], 401)
        cookie = self.request('/api/admin/login', {'password': self.s.config.password})[2]['Set-Cookie'].split(';')[0]
        status, body, _ = self.request('/api/admin/ranking', cookie=cookie)
        self.assertEqual(status, 200)
        entry_id = body['entries'][0]['id']
        self.assertEqual(self.request('/api/admin/ranking/delete', {'ids': [entry_id]}, cookie)[1]['entries'], [])

    def test_admin_clear_requires_confirmation(self):
        win(self.s, self.clock, 240)
        cookie = self.request('/api/admin/login', {'password': self.s.config.password})[2]['Set-Cookie'].split(';')[0]
        self.assertEqual(self.request('/api/admin/ranking/clear', {}, cookie)[0], 400)
        self.assertEqual(self.request('/api/admin/ranking/clear', {'confirm': True}, cookie)[1]['entries'], [])
