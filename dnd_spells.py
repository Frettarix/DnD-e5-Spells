import requests
from urllib.parse import urljoin
import json

from common import createLogger

logger = createLogger(__name__)


class Singleton():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class Parser(Singleton):
    @classmethod
    def __call__(cls):
        print('Parser')

class DBCarier(Singleton):
    @classmethod
    def __call__(cls):
        print('DB Worker')

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



class APICarier(Singleton):
    API_SPELLS_URL = 'https://www.dnd5eapi.co/api/spells'

    @classmethod
    def get_spells(cls) -> dict:
        logger.info('Getting data from API')

        _spells = cls.__api_request(cls.API_SPELLS_URL).json()

        spells = []
        for spell in _spells['results']:
            spells.append(
                cls.__api_request(
                    urljoin(cls.API_SPELLS_URL, spell['index'])
                ).json()
            )
        return {'spells': spells}

    @classmethod
    def __api_request(cls, url):
        logger.info(f'API request to {url}')
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
                logger.error(err)
                raise DndSpellsRequestError(resp.text)
        return resp

class CacheCarier(Singleton):
    cache_path = '.cached-spells'

    @classmethod
    def get_spells(cls) -> dict:
        logger.info('Getting data from cache')
        cached_spells = dict()
        try:
            with open(cls.cache_path, 'r') as f:
                cached_spells = json.load(f)
                logger.info('Got cached data')
        except (IOError, json.decoder.JSONDecodeError) as e:
            logger.warning(f'Can not get data from {cls.cache_path}: {e}')
        return cached_spells

    @classmethod
    def cache(cls, spells: dict):
        logger.info('Cache data')
        try:
            with open(cls.cache_path, 'w') as f:
                json.dump(spells, f)
        except IOError as e:
            logger.warning(f'Can not save token in {cls.cache_path}: {e}')

class Spells:
    def __init__(self, cache_carier=CacheCarier):
        self.api_carier = APICarier()
        self.cache_carier = cache_carier
        self.spells = self.__get_spells()
        self._cursor = 0

    def __get_spells(self):
        spells = self.cache_carier.get_spells()
        if not spells:
            spells = self.__normalize(
                self.api_carier.get_spells()
            )
            self.cache_carier.cache(spells)

        return Spells([Spell(**x) for x in spells['spells']])

    @classmethod
    def create_spell(cls, normed_spell: dict):
        """
        Firmats some of fields for simplification of working with Spell object
        normed_spell: dict from cache or API that was normalized before
        """

        normed_spell['class'] = [x['name'] for x in normed_spell.pop('classes')]
        normed_spell['desc'] = '\n'.join([line for line in normed_spell['desc']])
        normed_spell['higher_level'] = '\n'.join([line for line in normed_spell['higher_level']])
        normed_spell['school'] = [x['name'] for x in normed_spell.pop('school')]
        normed_spell['subclass'] = [x['name'] for x in normed_spell.pop('subclasses')]
        for x in normed_spell:
            x['damage_type'], x['damage_at_slot_level'] = None, None
            if (_damage := x.pop('damage')):
                x['damage_type'] = _damage['damage_type']['name']
                x['damage_at_slot_level'] = _damage.get('damage_at_slot_level')
            x['dexterity_type'], x['dexterity_success'], x['dexterity_desc'] = None, None, None
            if (_dc := x.pop('dc')):
                x['dexterity_type'] = _dc['dc_type']['name']
                x['dexterity_success'] = _dc.get('dc_success')
                x['dexterity_desc'] = _dc.get('desc')


    @classmethod
    def __normalize(cls, spells: dict):
        """ When spells comes from API it should be normaized before putting them into cache/database. This function does this.
        spells: {'spells': [ {'name': 'Acid Arrow', ...}, ]}
        """

        _all_fields = [list(spell.keys()) for spell in spells['spells']]
        all_fields = set([field for fields in _all_fields for field in fields])

        normalized_spells = {'spells': []}

        for spell in spells['spells']:
            spell_tmp = {f: spell.get(f) for f in all_fields}
            normalized_spells['spells'].append(spell_tmp)

        return normalized_spells

    def __iter__(self):
        return self

    def __next__(self):
        if self._cursor + 1 >= len(self.spells):
            raise StopIteration()
        self._cursor += 1

    def __str__(self):
        msg = '\n'.join([x.__str__() for x in self.spells])
        return f'{len(self.spells)} spells: \n{msg}'





class Spell:
    def __init__(self, **fields):
        for f in fields:
            if f == 'desc':
                self.desc = '\n'.join([x for x in fields[f]])
            elif f == 'classes':
                self.classes = [x['name'] for x in fields[f]]
            else:
                setattr(self, f, fields[f])

    def full_str(self):
        msg = '\n'
        for key, val in self.__dict__.items():
            msg += f'{key}: {val}\n'
        return msg

    def is_fit(self, filter: dict):
        """
        filter = {'name': 'acid arrow'}
        filter = {'level': 1, 'concentrate': True}
        """
        for key, val in filter.items():
            obj_field = getattr(self, key)
            if isinstance(obj_field, list):
                if val not in obj_field:
                    return False
            else:
                if getattr(self, key) != val:
                    return False
        return True

    def __str__(self):
        return f'"{self.name}" (classes: {", ".join([x for x in self.classes])}; level: {self.level}; ritual: {self.ritual}; concentration: {self.concentration})'




all_spells = get_spells()

spells = Spells([Spell(**x) for x in all_spells['spells']])
# print(spells)

fs = spells.get_by(character_class='druid', ritual=True, concentration='false')
print(fs)

d = APICarier()
d()

# result = []
# for x in spells:
#     if x.is_fit({'level': 2, 'ritual': True}):
#         result.append(x)
# print(spells[4].full_str())
# print(spells[0].is_fit({'level': 2, 'ritual': True}))

# print([x.full_str() for x in result])
# for x in result:
#     print(x)


# spell = Spell(**get_spell(all_the_spells['results'][0]['index']))
# print(spell)
# print(spell.__dict__)

