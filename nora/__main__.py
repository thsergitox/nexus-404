import sys
from .config import Config
from .conversation.provider import OpenAIProvider
from .game.station import Station
from .game.storage import StorageError
from .http import make_server
from .setup import setup


def main():
    if sys.argv[1:] == ['setup']:
        setup()
        return
    config = Config.environment()
    try:
        station = Station(config, OpenAIProvider(config))
        server = make_server(station)
    except (StorageError, OSError, ValueError) as error:
        print(f'No se pudo iniciar NORA: {error}', file=sys.stderr)
        sys.exit(1)
    print(f'NORA · http://localhost:{config.port} · Control privado: /facilitador')
    if not config.api_key:
        print('OpenAI sin configurar. El facilitador puede activar contingencia local.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
