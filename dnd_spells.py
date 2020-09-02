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
    def __call__(cls, q):
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
        return self.get_spells_by({'name': name})

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


spells = [
            {
            "level": 2,
            "heal_at_slot_level": None,
            "components": [
                "V",
                "S",
                "M"
            ],
            "attack_type": "ranged",
            "index": "acid-arrow",
            "subclasses": [
                {
                    "name": "Lore",
                    "url": "/api/subclasses/lore"
                },
                {
                    "name": "Land",
                    "url": "/api/subclasses/land"
                }
            ],
            "ritual": False,
            "range": "90 feet",
            "higher_level": [
                "When you cast this spell using a spell slot of 3rd level or higher, the damage (both initial and later) increases by 1d4 for each slot level above 2nd."
            ],
            "school": {
                "name": "Evocation",
                "url": "/api/magic-schools/evocation"
            },
            "concentration": False,
            "classes": [
                {
                    "name": "Wizard",
                    "url": "/api/classes/wizard"
                }
            ],
            "casting_time": "1 action",
            "duration": "Instantaneous",
            "desc": [
                "A shimmering green arrow streaks toward a target within range and bursts in a spray of acid. Make a ranged spell attack against the target. On a hit, the target takes 4d4 acid damage immediately and 2d4 acid damage at the end of its next turn. On a miss, the arrow splashes the target with acid for half as much of the initial damage and no damage at the end of its next turn."
            ],
            "material": "Powdered rhubarb leaf and an adder's stomach.",
            "url": "/api/spells/acid-arrow",
            "damage": {
                "damage_type": {
                    "name": "Acid",
                    "url": "/api/damage-types/acid"
                },
                "damage_at_slot_level": {
                    "2": "4d4",
                    "3": "5d4",
                    "4": "6d4",
                    "5": "7d4",
                    "6": "8d4",
                    "7": "9d4",
                    "8": "10d4",
                    "9": "11d4"
                }
            },
            "dc": None,
            "name": "Acid Arrow",
            "area_of_effect": None
        },
        {
            "level": 0,
            "heal_at_slot_level": None,
            "components": [
                "V",
                "S"
            ],
            "attack_type": None,
            "index": "acid-splash",
            "subclasses": [
                {
                    "name": "Lore",
                    "url": "/api/subclasses/lore"
                }
            ],
            "ritual": False,
            "range": "60 feet",
            "higher_level": None,
            "school": {
                "name": "Conjuration",
                "url": "/api/magic-schools/conjuration"
            },
            "concentration": False,
            "classes": [
                {
                    "name": "Sorcerer",
                    "url": "/api/classes/sorcerer"
                },
                {
                    "name": "Wizard",
                    "url": "/api/classes/wizard"
                }
            ],
            "casting_time": "1 action",
            "duration": "Instantaneous",
            "desc": [
                "You hurl a bubble of acid. Choose one creature within range, or choose two creatures within range that are within 5 feet of each other. A target must succeed on a dexterity saving throw or take 1d6 acid damage.",
                "This spell's damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6)."
            ],
            "material": None,
            "url": "/api/spells/acid-splash",
            "damage": {
                "damage_type": {
                    "name": "Acid",
                    "url": "/api/damage-types/acid"
                },
                "damage_at_character_level": {
                    "1": "1d6",
                    "5": "2d6",
                    "11": "3d6",
                    "17": "4d6"
                }
            },
            "dc": {
                "dc_type": {
                    "name": "DEX",
                    "url": "/api/ability-scores/dex"
                },
                "dc_success": "none"
            },
            "name": "Acid Splash",
            "area_of_effect": None
        }
        ]

filters = {'level': 2, 'class': 'Wizard'}
s = Spells(spells=spells)
# print(s)
res = s.get_spells_by(filters)
print(res)
# d2.get_spells_by