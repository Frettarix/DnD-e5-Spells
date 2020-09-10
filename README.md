# D&D Spells Bot for Telegram

## About

Welcome, adventurer!

D&D Spells Bot helps you to find the best 5e spells for you awkward conditions.

Send */class \<class>* message to let the bot know what is your class. Next you can search for spells using */spellnamed* and */searchspell* commands.

Bot: [@dnd_5e_spells_bot](https://t.me/dnd_5e_spells_bot)

Author: [@lisp3r](https://t.me/lisp3r)

Source: [DnD-e5-Spells](https://github.com/lisp3r/DnD-e5-Spells)

## Usage

/class *\<your class\>*

**Examples:**

- /class

  Reset saved class

- /class Warlock

  Set class Warlock

/spellnamed *\<spell name\>*

**Examples:**

- /spellnamed acid arrow

  Return Acid Arrow full description

- /spellnamed acid

  Return links to all the spells with'acid' in name

/searchspell *\<filters\>*

**Examples:**

- /searchspell

  Return all spells for your class if specifiedor all spells

- /searchspell level=2 & ritual=true

  Command with filters and boolean *AND* operator gets satisfying spells.

**Filters:**

- level _int_
- ritual _bool_
- concentration _bool_

/settings - show user's settings

/help - this help

## Spells API

The bot uses [D&D 5e API](www.dnd5eapi.co). See [doc page](http://www.dnd5eapi.co/docs/) for more information.
