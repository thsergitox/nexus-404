"""Preparación local sin publicar ni imprimir credenciales."""
import secrets
from .config import ROOT


def setup():
    target = ROOT / '.env'
    if target.exists():
        print('Ya existe .env; se conserva sin cambios.')
        return
    password = secrets.token_urlsafe(24)
    content = (ROOT / '.env.example').read_text().replace('FACILITATOR_PASSWORD=', 'FACILITATOR_PASSWORD=' + password)
    with target.open('x') as file:
        file.write(content)
    target.chmod(0o600)
    print('Configuración creada en .env (permiso 600). Consulte allí FACILITATOR_PASSWORD para entrar al control privado.')
    print('Añada OPENAI_API_KEY en ese archivo o en el entorno del servidor; nunca en el chat.')
