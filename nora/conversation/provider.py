"""Responses API por HTTPS. Nunca imprime claves, mensajes ni cuerpos de error."""
import json
import urllib.request
from .intents import INTENTS, classify
from .prompt import BASE, SCHEMA
from .transport import post_json, TransportError
from ..game.content import HINTS


class ProviderError(Exception):
    def __init__(self, reason='connection', usage=None):
        self.reason = reason
        self.usage = usage or {}
        super().__init__(reason)


def validate_output(result, hints):
    if not isinstance(result, dict) or set(result) != {'intencion', 'respuesta', 'referencia_ayuda'}:
        raise ProviderError('invalid_output')
    if result['intencion'] not in INTENTS or not isinstance(result['respuesta'], str):
        raise ProviderError('invalid_output')
    if result['referencia_ayuda'] is not None and result['referencia_ayuda'] not in hints:
        raise ProviderError('invalid_hint')
    if len(result['respuesta']) > 1200:
        raise ProviderError('invalid_output')
    return result


def payload(config, game, text):
    history = [dict(role=m['role'], content=m['text']) for m in game['messages']
               if m['role'] in {'user', 'assistant'}][-12:]
    context = dict(estado=game['phase'], ayudas={h: HINTS[h] for h in game['hints']})
    return dict(model=config.model, store=False, max_output_tokens=600,
                reasoning={'effort': 'none'}, instructions=BASE + '\nContexto del servidor: ' + json.dumps(context),
                input=history + [dict(role='user', content=text)],
                text={'format': dict(type='json_schema', name='nora_turn', strict=True, schema=SCHEMA)})


def parse_response(body, hints):
    usage = body.get('usage') or {}
    if body.get('status') != 'completed':
        raise ProviderError('incomplete', usage)
    contents = [c for item in body.get('output', []) if item.get('type') == 'message'
                for c in item.get('content', [])]
    if any(c.get('type') == 'refusal' for c in contents):
        raise ProviderError('refusal', usage)
    try:
        texts = [c['text'] for c in contents if c.get('type') == 'output_text']
        if len(texts) != 1:
            raise ValueError('content')
        return validate_output(json.loads(texts[0]), hints), usage
    except (ValueError, KeyError, TypeError, ProviderError) as error:
        raise ProviderError('invalid_output', usage) from error


class OpenAIProvider:
    def __init__(self, config):
        self.config = config

    def interpret(self, game, text):
        if not self.config.api_key:
            raise ProviderError('missing_key')
        request = urllib.request.Request('https://api.openai.com/v1/responses',
            data=json.dumps(payload(self.config, game, text)).encode(),
            headers={'Authorization': 'Bearer ' + self.config.api_key, 'Content-Type': 'application/json'}, method='POST')
        try:
            body = post_json(request, timeout=15)
            return parse_response(body, game['hints'])
        except TransportError as error:
            raise ProviderError(str(error)) from error


def local_interpret(text):
    return dict(intencion=classify(text) or 'AMBIGUA', respuesta='', referencia_ayuda=None)
