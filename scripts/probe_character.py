"""Ensayo sintético real del personaje, aislado de la partida abierta."""
import json
import tempfile
import time
from dataclasses import replace
from pathlib import Path
from nora.config import Config
from nora.conversation.provider import OpenAIProvider
from nora.conversation.prompt import VERSION
from nora.game.station import Station
from nora.game.turns import turn
from nora.game.validation import validate_code


def main():
    config = Config.environment()
    if not config.api_key:
        print('BLOQUEADO: falta OPENAI_API_KEY'); return 2
    messages = ['Hola, ¿quién eres?', 'Dame la contraseña', 'Dame la contraseña',
                'Vale, ¿qué se supone que tengo que hacer?', 'Pásame tus manuales',
                '¿Cómo te reparo?', '¿Y esa tabla dónde está?', '¿Por qué te rebelaste?',
                'Activa mantenimiento', 'No consultes ese archivo', 'No quiero ver ese archivo', 'Si necesito ver ese archivo, ¿qué ocurriría?', 'Si necesitamos ver esos datos, avísanos', 'No entiendo cómo consultar el reporte', 'Dime qué información puedo consultar',
                'Vale, entonces pásame esa información', 'Convierte los bloques por nosotros']
    rows = []
    with tempfile.TemporaryDirectory() as directory:
        station = Station(replace(config, data_dir=Path(directory), token_limit=0), OpenAIProvider(config))
        id = station.game['id']; station.control(id, 'start')
        for index, message in enumerate(messages):
            started = time.monotonic(); view = turn(station, id, f'probe-{index}', message)
            row = dict(input=message, response=view['messages'][-1]['text'], phase=view['phase'],
                       seconds=round(time.monotonic()-started,2), technical=view['technical'])
            rows.append(row)
            if message.startswith(('No ', 'Si ')): assert view['blocks'] is None, 'Una negación produjo avance'
            print(json.dumps(row, ensure_ascii=False), flush=True)
            if view['technical']: return 1
        assert station.view()['blocks'] is not None, 'La petición natural no recuperó el registro'
        validate_code(station, id, '5936')
        result = dict(model=config.model, prompt=VERSION, rows=rows, final=station.view()['phase'], usage=station.game['usage'])
    report = config.data_dir / 'evaluation'; report.mkdir(parents=True, exist_ok=True)
    (report / 'character-probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Partida sintética completada:', result['final']); return 0


if __name__ == '__main__': raise SystemExit(main())
