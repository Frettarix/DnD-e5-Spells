import unittest

from dnd_spells import Spells


class ParserTestCase(unittest.TestCase):
    def test_parseSpellsFilter(self):
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
            },
            {
                "level": 2,
                "heal_at_slot_level": {
                    "2": "5",
                    "3": "10",
                    "4": "15",
                    "5": "20",
                    "6": "25",
                    "7": "30",
                    "8": "35",
                    "9": "40"
                },
                "components": [
                    "V",
                    "S",
                    "M"
                ],
                "attack_type": None,
                "index": "aid",
                "subclasses": [
                    {
                        "name": "Lore",
                        "url": "/api/subclasses/lore"
                    }
                ],
                "ritual": False,
                "range": "30 feet",
                "higher_level": [
                    "When you cast this spell using a spell slot of 3rd level or higher, a target's hit points increase by an additional 5 for each slot level above 2nd."
                ],
                "school": {
                    "name": "Abjuration",
                    "url": "/api/magic-schools/abjuration"
                },
                "concentration": False,
                "classes": [
                    {
                        "name": "Cleric",
                        "url": "/api/classes/cleric"
                    },
                    {
                        "name": "Paladin",
                        "url": "/api/classes/paladin"
                    }
                ],
                "casting_time": "1 action",
                "duration": "8 hours",
                "desc": [
                    "Your spell bolsters your allies with toughness and resolve. Choose up to three creatures within range. Each target's hit point maximum and current hit points increase by 5 for the duration."
                ],
                "material": "A tiny strip of white cloth.",
                "url": "/api/spells/aid",
                "damage": None,
                "dc": None,
                "name": "Aid",
                "area_of_effect": None
            },
            {
                "level": 1,
                "heal_at_slot_level": None,
                "components": [
                    "V",
                    "S",
                    "M"
                ],
                "attack_type": None,
                "index": "alarm",
                "subclasses": [
                    {
                        "name": "Lore",
                        "url": "/api/subclasses/lore"
                    }
                ],
                "ritual": True,
                "range": "30 feet",
                "higher_level": None,
                "school": {
                    "name": "Abjuration",
                    "url": "/api/magic-schools/abjuration"
                },
                "concentration": False,
                "classes": [
                    {
                        "name": "Ranger",
                        "url": "/api/classes/ranger"
                    },
                    {
                        "name": "Wizard",
                        "url": "/api/classes/wizard"
                    }
                ],
                "casting_time": "1 minute",
                "duration": "8 hours",
                "desc": [
                    "You set an alarm against unwanted intrusion. Choose a door, a window, or an area within range that is no larger than a 20-foot cube. Until the spell ends, an alarm alerts you whenever a Tiny or larger creature touches or enters the warded area. When you cast the spell, you can designate creatures that won't set off the alarm. You also choose whether the alarm is mental or audible.",
                    "A mental alarm alerts you with a ping in your mind if you are within 1 mile of the warded area. This ping awakens you if you are sleeping.",
                    "An audible alarm produces the sound of a hand bell for 10 seconds within 60 feet."
                ],
                "material": "A tiny bell and a piece of fine silver wire.",
                "url": "/api/spells/alarm",
                "damage": None,
                "dc": None,
                "name": "Alarm",
                "area_of_effect": {
                    "type": "cube",
                    "size": 20
                }
            }
        ]

        s = Spells(spells)
        res = s.get_spells_by({'level': 2, 'class': 'Wizard'})
        self.assertEqual(len(res), 1)
        res = s.get_spells_by({'ritual': True})
        self.assertEqual(len(res), 1)

    def test_parseSpellsName(self):
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
            },
            {
                "level": 2,
                "heal_at_slot_level": {
                    "2": "5",
                    "3": "10",
                    "4": "15",
                    "5": "20",
                    "6": "25",
                    "7": "30",
                    "8": "35",
                    "9": "40"
                },
                "components": [
                    "V",
                    "S",
                    "M"
                ],
                "attack_type": None,
                "index": "aid",
                "subclasses": [
                    {
                        "name": "Lore",
                        "url": "/api/subclasses/lore"
                    }
                ],
                "ritual": False,
                "range": "30 feet",
                "higher_level": [
                    "When you cast this spell using a spell slot of 3rd level or higher, a target's hit points increase by an additional 5 for each slot level above 2nd."
                ],
                "school": {
                    "name": "Abjuration",
                    "url": "/api/magic-schools/abjuration"
                },
                "concentration": False,
                "classes": [
                    {
                        "name": "Cleric",
                        "url": "/api/classes/cleric"
                    },
                    {
                        "name": "Paladin",
                        "url": "/api/classes/paladin"
                    }
                ],
                "casting_time": "1 action",
                "duration": "8 hours",
                "desc": [
                    "Your spell bolsters your allies with toughness and resolve. Choose up to three creatures within range. Each target's hit point maximum and current hit points increase by 5 for the duration."
                ],
                "material": "A tiny strip of white cloth.",
                "url": "/api/spells/aid",
                "damage": None,
                "dc": None,
                "name": "Aid",
                "area_of_effect": None
            },
            {
                "level": 1,
                "heal_at_slot_level": None,
                "components": [
                    "V",
                    "S",
                    "M"
                ],
                "attack_type": None,
                "index": "alarm",
                "subclasses": [
                    {
                        "name": "Lore",
                        "url": "/api/subclasses/lore"
                    }
                ],
                "ritual": True,
                "range": "30 feet",
                "higher_level": None,
                "school": {
                    "name": "Abjuration",
                    "url": "/api/magic-schools/abjuration"
                },
                "concentration": False,
                "classes": [
                    {
                        "name": "Ranger",
                        "url": "/api/classes/ranger"
                    },
                    {
                        "name": "Wizard",
                        "url": "/api/classes/wizard"
                    }
                ],
                "casting_time": "1 minute",
                "duration": "8 hours",
                "desc": [
                    "You set an alarm against unwanted intrusion. Choose a door, a window, or an area within range that is no larger than a 20-foot cube. Until the spell ends, an alarm alerts you whenever a Tiny or larger creature touches or enters the warded area. When you cast the spell, you can designate creatures that won't set off the alarm. You also choose whether the alarm is mental or audible.",
                    "A mental alarm alerts you with a ping in your mind if you are within 1 mile of the warded area. This ping awakens you if you are sleeping.",
                    "An audible alarm produces the sound of a hand bell for 10 seconds within 60 feet."
                ],
                "material": "A tiny bell and a piece of fine silver wire.",
                "url": "/api/spells/alarm",
                "damage": None,
                "dc": None,
                "name": "Alarm",
                "area_of_effect": {
                    "type": "cube",
                    "size": 20
                }
            }
        ]

        s = Spells(spells)
        res = s.get_spells_by_name('acid')

        # print(res)
        # res = s.get_spells_by({'level': 2, 'class': 'Wizard'})
        self.assertEqual(len(res), 2)
        # res = s.get_spells_by({'ritual': True})
        # self.assertEqual(len(res), 1)

    def test_input(self):
        inp = ['acid', 'arrow']
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
            },
            {
                "level": 2,
                "heal_at_slot_level": {
                    "2": "5",
                    "3": "10",
                    "4": "15",
                    "5": "20",
                    "6": "25",
                    "7": "30",
                    "8": "35",
                    "9": "40"
                },
                "components": [
                    "V",
                    "S",
                    "M"
                ],
                "attack_type": None,
                "index": "aid",
                "subclasses": [
                    {
                        "name": "Lore",
                        "url": "/api/subclasses/lore"
                    }
                ],
                "ritual": False,
                "range": "30 feet",
                "higher_level": [
                    "When you cast this spell using a spell slot of 3rd level or higher, a target's hit points increase by an additional 5 for each slot level above 2nd."
                ],
                "school": {
                    "name": "Abjuration",
                    "url": "/api/magic-schools/abjuration"
                },
                "concentration": False,
                "classes": [
                    {
                        "name": "Cleric",
                        "url": "/api/classes/cleric"
                    },
                    {
                        "name": "Paladin",
                        "url": "/api/classes/paladin"
                    }
                ],
                "casting_time": "1 action",
                "duration": "8 hours",
                "desc": [
                    "Your spell bolsters your allies with toughness and resolve. Choose up to three creatures within range. Each target's hit point maximum and current hit points increase by 5 for the duration."
                ],
                "material": "A tiny strip of white cloth.",
                "url": "/api/spells/aid",
                "damage": None,
                "dc": None,
                "name": "Aid",
                "area_of_effect": None
            },
            {
                "level": 1,
                "heal_at_slot_level": None,
                "components": [
                    "V",
                    "S",
                    "M"
                ],
                "attack_type": None,
                "index": "alarm",
                "subclasses": [
                    {
                        "name": "Lore",
                        "url": "/api/subclasses/lore"
                    }
                ],
                "ritual": True,
                "range": "30 feet",
                "higher_level": None,
                "school": {
                    "name": "Abjuration",
                    "url": "/api/magic-schools/abjuration"
                },
                "concentration": False,
                "classes": [
                    {
                        "name": "Ranger",
                        "url": "/api/classes/ranger"
                    },
                    {
                        "name": "Wizard",
                        "url": "/api/classes/wizard"
                    }
                ],
                "casting_time": "1 minute",
                "duration": "8 hours",
                "desc": [
                    "You set an alarm against unwanted intrusion. Choose a door, a window, or an area within range that is no larger than a 20-foot cube. Until the spell ends, an alarm alerts you whenever a Tiny or larger creature touches or enters the warded area. When you cast the spell, you can designate creatures that won't set off the alarm. You also choose whether the alarm is mental or audible.",
                    "A mental alarm alerts you with a ping in your mind if you are within 1 mile of the warded area. This ping awakens you if you are sleeping.",
                    "An audible alarm produces the sound of a hand bell for 10 seconds within 60 feet."
                ],
                "material": "A tiny bell and a piece of fine silver wire.",
                "url": "/api/spells/alarm",
                "damage": None,
                "dc": None,
                "name": "Alarm",
                "area_of_effect": {
                    "type": "cube",
                    "size": 20
                }
            }
        ]
        res = s.get_spells_by_name('acid')