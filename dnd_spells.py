import requests
from urllib.parse import urljoin
import json

from common import createLogger

logger = createLogger(__name__)


class DndSpellsError(Exception):
    pass

class DndSpellsRequestError(DndSpellsError):
    def __init__(self, body):
        self.body = json.loads(body)
        self.status = self.body["error"]["status"]
        self.message = self.body["error"]["message"]
        self.reason = self.body["error"].get("reason")
    def __str__(self):
        return f'{self.body}'


def get_cached_spells(cache_path='.cached-spells') -> dict:
    cached_spells = dict()
    try:
        with open(cache_path, 'r') as f:
            cached_spells = json.load(f)
            logger.info('Got cached data')
    except (IOError, json.decoder.JSONDecodeError) as e:
        logger.warning(f'Can not get data from {cache_path}: {e}')
    return cached_spells

def cache_spells(spells: dict, cache_path) -> None:
    logger.info('Cache data')
    try:
        with open(cache_path, 'w') as f:
            json.dump(spells, f)
    except IOError as e:
        logger.warning(f'Can not save token in {cache_path}: {e}')

def api_request(url_path, method):
    API_URL = 'https://www.dnd5eapi.co/api/'
    url = urljoin(API_URL, url_path)
    logger.info(f'API request to {url}')

    try:
        resp = requests.request(method=method, url = url)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
            logger.error(err)
            raise DndSpellsRequestError(resp.text)
    return resp

def get_spells_from_API():
    logger.info('Getting data from API')
    spells_url_path = 'spells/'
    _spells = api_request(spells_url_path, 'GET').json()

    spells = []
    for spell in _spells['results']:
        spells.append(
            api_request(urljoin(spells_url_path, spell['index']), 'GET').json()
        )
    # print(spells)
    return {'spells': spells}

def get_spells(spell=None, cache=True, cache_path='.cached-spells') -> dict:
    """
    Getting D&D 5e spells

    spell:      Specific spell to search for. Example: acid-arrow
    cache:      Do we cache the results?
    cache_path: Path to cache file.

    return: dict with spell(s)
    """
    spells = get_cached_spells(cache_path)

    if not spells:
        spells = get_spells_from_API()

        if cache:
            cache_spells(spells, cache_path)

    if spell:
        for _s in spells:
            if spell.lower() == _s['name'].lower():
                return _s
        logger.error(f'No {spell} in spells')
        raise DndSpellsError(f'No {spell} in spells')
    return spells

class Spell:
    def __init__(self, **fields):
        for f in fields:
            if f == 'desc':
                self.desc = '\n'.join([x for x in fields[f]])
            setattr(self, f, fields[f])

    def full_str(self):
        msg = '\n'
        for key, val in self.__dict__.items():
            msg += f'{key}: {val}\n'
        return msg

    def is_fit(self, filter: dict):
        field, val = filter.items()
        fields = list(vars(self).keys()
        if field in fields:
            if getattr(self, field) == val:
                return True
        return False

    def __str__(self):
        return f'{self.name}'


all_spells = get_spells()
# print(all_spells)
for x in all_spells['spells']:
    print(Spell(**x).full_str())


# spell = Spell(**get_spell(all_the_spells['results'][0]['index']))
# print(spell)
# print(spell.__dict__)

