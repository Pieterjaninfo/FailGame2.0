import json
from time import strftime

SETTINGS_FILE = 'settings.conf'
LOG_FILE = 'logs.txt'


def load_data(game):
    try:
        with open(SETTINGS_FILE, 'r') as f:
            data = json.loads(f.read())
        if 'score' in data:
            game.score = data['score']
    except json.decoder.JSONDecodeError:
        log('INVALID SETTINGS CONFIGURATION FILE - Please empty this file and restart program!')


def store_data(game):
    data = {
        'score': game.score
    }
    with open(SETTINGS_FILE, 'w') as f:
        f.write(json.dumps(data))


def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(strftime('%d/%m/%Y-%H:%M:%S') + ' | ' + msg + '\n')
