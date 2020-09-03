import requests
from urllib.parse import urljoin
import json
import re

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


class Singleton():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

class Parser(Singleton):
    """
    root ::= value
    value ::= string | filter | '&'
    filter ::= string '=' value
    """

    @classmethod
    def __call__(cls, q, _type):
        result = {}
        while q:
            field, value, q = list(cls.__parse_filter(q))
            result.update({field: value})
        return result

    @classmethod
    def __parse_filter(cls, q):
        filter_regex = re.compile(r'(\w+)\s*=\s*([a-zA-Z0-9_ ]*)\s*(.*)')
        match = filter_regex.search(q)
        if match is not None:
            field, value, remainds = match.groups()
            return field.strip(), value.strip(), remainds

class DBCarier(Singleton):
    @classmethod
    def __call__(cls):
        print('DB Worker')


class APICarier(Singleton):
    API_SPELLS_URL = 'https://www.dnd5eapi.co/api/spells/'

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
    def __init__(self, spells=None, cache_carier=CacheCarier()):
        self.__api_carier = APICarier()
        self.__cache_carier = cache_carier
        self.spells = spells
        self._cursor = 0

    @classmethod
    def __update_cache(self):
        pass

    @property
    def spells(self):
        return self.__spells

    @spells.setter
    def spells(self, _spells=None):
        if _spells:
            assert isinstance(_spells, list)
            if isinstance(_spells[0], Spell):
                self.__spells = _spells
            elif isinstance(_spells[0], dict):
                self.__spells = [self.create_spell(x) for x in _spells]
        else:
            if _spells == []:
                self.__spells = []
            else:
                spells = self.__cache_carier.get_spells()
                if not spells:
                    spells = self.__normalize(
                        self.__api_carier.get_spells()
                    )
                    self.__cache_carier.cache(spells)
                self.__spells = [self.create_spell(x) for x in spells['spells']]

    def get_spells_by(self, filters):
        if 'class' in filters:
            filters['classes'] = filters.pop('class')
        res_spells = []
        for spell in self.__spells:
            if spell.is_fit(filters):
                res_spells.append(spell)
        return Spells(spells=res_spells)

    def get_spells_by_name(self, name):
        name = ' '.join([x.capitalize() for x in name.split()])
        if (res_spell := self.get_spells_by({'name': name})):
            return res_spell
        else:
            res_spells = []
            for s in self.spells:
                if name in s.name:
                    res_spells.append(s)
            return Spells(spells=res_spells)

    @classmethod
    def create_spell(cls, normed_spell: dict):
        """
        Firmats some of fields for simplification of working with Spell object
        normed_spell: dict from cache or API that was normalized before
        """
        normed_spell['classes'] = [x['name'] for x in normed_spell.pop('classes')]
        normed_spell['desc'] = '\n'.join([line for line in normed_spell.pop('desc')])
        if normed_spell['higher_level']:
            normed_spell['higher_level'] = '\n'.join([line for line in normed_spell.pop('higher_level')])
        normed_spell['school'] = normed_spell['school']['name']
        normed_spell['subclass'] = [x['name'] for x in normed_spell.pop('subclasses')]

        normed_spell['damage_type'], normed_spell['damage_at_slot_level'] = None, None
        if (_damage := normed_spell.pop('damage')):
            _damage_name = _damage.get('damage_type')
            if _damage_name:
                normed_spell['damage_type'] = _damage_name['name']
            normed_spell['damage_at_slot_level'] = _damage.get('damage_at_slot_level')
            normed_spell['damage_at_character_level'] = _damage.get('damage_at_character_level')

        normed_spell['dexterity_type'], normed_spell['dexterity_success'], normed_spell['dexterity_desc'] = None, None, None
        if (_dc := normed_spell.pop('dc')):
            normed_spell['dexterity_type'] = _dc['dc_type']['name']
            normed_spell['dexterity_success'] = _dc.get('dc_success')
            normed_spell['dexterity_desc'] = _dc.get('desc')
        return Spell(**normed_spell)

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
        if self._cursor + 1 >= len(self.__spells):
            raise StopIteration()
        self._cursor += 1

    def __str__(self):
        msg = '\n'.join([x.__str__() for x in self.__spells])
        return f'{len(self.__spells)} spells: \n{msg}'

    def __len__(self):
        return len(self.spells)

class Spell:
    def __init__(self, **fields):
        for f in fields: setattr(self, f, fields[f])

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
        # return f'"{self.name}": {self.classes}'
        return f'"{self.name}" (classes: {", ".join([x for x in self.classes])}; level: {self.level}; ritual: {self.ritual}; concentration: {self.concentration})'

s = Spells()
inp = ['water']
res = s.get_spells_by_name(' '.join(inp))
print(res)