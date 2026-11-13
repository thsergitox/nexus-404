"""Configuración exclusivamente del servidor."""
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_environment(path=ROOT / '.env'):
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip() and not line.lstrip().startswith('#') and '=' in line:
                name, value = line.split('=', 1)
                os.environ.setdefault(name.strip(), value.strip())


@dataclass(frozen=True)
class Config:
    data_dir: Path
    password: str = ''
    api_key: str = ''
    model: str = 'gpt-5.6-terra'
    token_limit: int = 0
    strict: bool = False
    port: int = 4040

    @classmethod
    def environment(cls):
        load_environment()
        return cls(
            Path(os.getenv('NORA_DATA_DIR', str(ROOT / 'data'))),
            os.getenv('FACILITATOR_PASSWORD', ''), os.getenv('OPENAI_API_KEY', ''),
            os.getenv('OPENAI_MODEL', 'gpt-5.6-terra'),
            int(os.getenv('EVENT_TOKEN_LIMIT', '0')),
            os.getenv('NORA_STRICT_CATALOG', '0') == '1',
            int(os.getenv('PORT', '4040')),
        )
