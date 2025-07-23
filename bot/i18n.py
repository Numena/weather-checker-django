import json
from pathlib import Path

_LOCALES_PATH = Path(__file__).with_suffix('').parent / 'locales'
_CACHE = {}

def _load(locale: str) -> dict:
    if locale not in _CACHE:
        path = _LOCALES_PATH / f'{locale}.json'
        _CACHE[locale] = json.loads(path.read_text(encoding='utf-8'))
    return _CACHE[locale]

def tr(key: str, locale: str, **kwargs) -> str:
    data = _load(locale)
    template = data.get(key, key)
    return template.format(**kwargs)