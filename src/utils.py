'''
## Attributes
user_config: dict
'''

from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json

config_path = Path(__file__).parent.parent / 'config.json'

with open(config_path, 'r') as config:
    user_config: dict = json.loads(config.read())
