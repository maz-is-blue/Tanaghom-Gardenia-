import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(_HERE, '..', 'content')


def load(name, default=None):
    path = os.path.join(CONTENT_DIR, name + '.json')
    if not os.path.exists(path):
        return default if default is not None else {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save(name, data):
    path = os.path.join(CONTENT_DIR, name + '.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all():
    audio_data = load('audio', {'tracks': []})
    audio_by_id = {t['id']: t for t in audio_data.get('tracks', [])}
    return {
        'settings': load('settings', {}),
        'home':     load('home', {}),
        'about':    load('about', {}),
        'gallery':  load('gallery', {'items': []}),
        'audio':    audio_data,
        'audio_by_id': audio_by_id,
    }
