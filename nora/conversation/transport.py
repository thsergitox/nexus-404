"""Límite total independiente del timeout de cada operación del socket."""
import json
import queue
import threading
from urllib.request import urlopen


class TransportError(Exception):
    pass


def post_json(request, timeout=15):
    result = queue.Queue(maxsize=1)

    def request_body():
        try:
            with urlopen(request, timeout=timeout) as response:
                raw = response.read(200_001)
            if len(raw) > 200_000:
                raise ValueError('response_size')
            result.put((json.loads(raw), None))
        except Exception:
            result.put((None, 'connection'))

    threading.Thread(target=request_body, daemon=True).start()
    try:
        body, error = result.get(timeout=timeout)
    except queue.Empty as error:
        raise TransportError('timeout') from error
    if error or not isinstance(body, dict):
        raise TransportError('connection')
    return body
