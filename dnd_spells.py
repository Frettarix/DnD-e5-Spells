import requests
from urllib.parse import urljoin
import json
import logging


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


def createLogger(name, lvl=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = createLogger(__name__)


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

    spells = dict()
    for spell in _spells['results']:
        spells.update(
            api_request(urljoin(spells_url_path, spell['index']), 'GET').json()
        )
    # print(spells)
    return spells

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

# class Spell:
#     def __init__(self, **fields):
#         for x in fields:
#             setattr(self, x, fields[x])

#     def __str__(self):
#         return f'{self.name}\nlevel: {self.level}\nschool: {self.school["name"]}'

# class Spell:
#     def __init__(self, index: str, name: str, desc: list, higher_level: list,
#                     page: str, range: str, components: str, material: str, ritual: str,
#                     duration: str, concentration: str, casting_time: str, level: str,
#                     school: dict, classes: list, subclasses: list, url: str):
#         self.index = index
#         self.name = name
#         self.desc = desc
#         self.higher_level = higher_level
#         self.page = page
#         self.range = range
#         self.components = components
#         self.material = material
#         self.ritual = ritual
#         self.duration = duration
#         self.concentration = concentration
#         self.casting_time = casting_time
#         self.level =level
#         self.school = school
#         self.classes = classes
#         self.subclasses = subclasses
#         self.url = url

class Spell:
    def __init__(self, index: str, name: str, desc: list, higher_level: list,
                    page: str, range: str, components: str, material: str, ritual: str,
                    duration: str, concentration: str, casting_time: str, level: str,
                    school: dict, classes: list, subclasses: list, url: str):
        self.index = index
        self.name = name
        self.desc = desc
        self.higher_level = higher_level
        self.page = page
        self.range = range
        self.components = components
        self.material = material
        self.ritual = ritual
        self.duration = duration
        self.concentration = concentration
        self.casting_time = casting_time
        self.level =level
        self.school = school
        self.classes = classes
        self.subclasses = subclasses
        self.url = url


    def __str__(self):
        return f'{self.name}\nlevel: {self.level}\nschool: {self.school["name"]}'


all_spells = get_spells()
# print(all_spells)
# for x in all_the_spells['results']:
#     print(x)
    # Spell(**x)


# spell = Spell(**get_spell(all_the_spells['results'][0]['index']))
# print(spell)
# print(spell.__dict__)

