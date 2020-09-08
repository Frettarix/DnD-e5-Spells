import threading
from telegram import Bot, Update, ParseMode, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
import random
import time

from setup import TOKEN
# from database import save_to_mongo, DatabaseUnavaliable

from common import createLogger
from dnd_spells import Parser, Spells, Spell


magic_wand = '🪄'

logger = createLogger(__name__)
spells = Spells()

def send_message(bot, chat_id, text: str, **kwargs):
    MAX_MESSAGE_LENGTH = 4048

    if len(text) <= MAX_MESSAGE_LENGTH:
        return bot.send_message(chat_id, text, **kwargs)

    parts = []
    while len(text) > 0:
        if len(text) > MAX_MESSAGE_LENGTH:
            part = text[:MAX_MESSAGE_LENGTH]
            first_lnbr = part.rfind('\n')
            if first_lnbr != -1:
                parts.append(part[:first_lnbr])
                text = text[first_lnbr:]
            else:
                parts.append(part)
                text = text[MAX_MESSAGE_LENGTH:]
        else:
            parts.append(text)
            break
    msg = None
    for part in parts:
        msg = bot.send_message(chat_id, part, **kwargs)
        time.sleep(1)
    return msg  # return only the last message

def overall_logging(handler):
    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message') and hasattr(update, 'effective_user'):
            log_info = {
                'time': str(update.message.date),
                'handler': handler.__name__,
                'update_id': update.update_id,
                'message': {
                    'message_id': update.message.message_id,
                    'text': update.message.text,
                },
                'user': {
                    'user_id': update.effective_user.id,
                    'username': update.effective_user.username
                }
            }
            logger.info(log_info)
        return handler(*args, **kwargs)
    return inner

def print_spell(spell: dict):
    msg = f"""{magic_wand} *{spell['name']}*

{spell['desc']}

class: {', '.join([x for x in spell['classes']])}
subclass: {', '.join([x for x in spell['subclass']])}
school: {spell['school']}
"""

    for field in spell:
        if field not in ['name', 'classes', 'subclass', 'school', 'desc', 'url', 'index']:
            _val = spell[field]
            if _val:
                if isinstance(_val, list):
                    _val = ', '.join([x for x in _val])
                msg += f'{field.replace("_", " ")}: {_val}\n'
    return msg

def replay_for_class(user_class):
    bard = ['🪕', '🎸👨‍🎤']
    cleric = ['🙏']
    druid = ['🌿', '🌱', '🍄']
    barbarian = ['🪓', '🤬']
    monk = ['🧘', '🧘🏻', '🧘🏼', '🧘🏽', '🧘🏾', '🧘🏿', '🧘‍♂️', '🧘🏻‍♂️', '🧘🏼‍♂️', '🧘🏽‍♂️', '🧘🏾‍♂️', '🧘🏿‍♂️', '🧘‍♀️', '🧘🏻‍♀️', '🧘🏼‍♀️', '🧘🏽‍♀️', '🧘🏾‍♀️', '🧘🏿‍♀️']
    ranger = ['🏹']
    rogue = ['🔪']
    fighter = ['🗡️', '⚔️']
    paladin = [*fighter, '🛡️', '🌅']
    wizard = ['🧙', '🧙🏻', '🧙🏼', '🧙🏽', '🧙🏾', '🧙🏿', '🧙‍♂️', '🧙🏻‍♂️', '🧙🏼‍♂️', '🧙🏽‍♂️', '🧙🏾‍♂️', '🧙🏿‍♂️', '🧙‍♀️', '🧙🏻‍♀️', '🧙🏼‍♀️', '🧙🏽‍♀️', '🧙🏾‍♀️', '🧙🏿‍♀️', '⚗️', '📜', '🔮']
    if user_class.lower() == 'bard':
        return random.choice(bard)
    elif user_class.lower() == 'cleric':
        return random.choice(cleric)
    elif user_class.lower() == 'barbarian':
        return random.choice(barbarian)
    elif user_class.lower() == 'druid':
        return random.choice(druid)
    elif user_class.lower() == 'monk':
        return random.choice(monk)
    elif user_class.lower() == 'ranger':
        return random.choice(ranger)
    elif user_class.lower() == 'rogue':
        return random.choice(rogue)
    elif user_class.lower() == 'paladin':
        return random.choice(paladin)
    elif user_class.lower() == 'fighter':
        return random.choice(fighter)
    elif user_class.lower() in ['wizard', 'sorcerer', 'warlock']:
        return random.choice(wizard)

@overall_logging
def help_msg(update: Update, context: CallbackContext):
    help_text = """/class <your class> - set your class
/spellbyname <spell name>

    *Examples:*

        • /spellbyname acid arrow
          Command returns Acid Arrow full description

        • /spellbyname acid
          Command returns links to all the spells with 'acid' in name

/spellsearch <filters>

    *Examples:*

        • /spellsearch level=2 & ritual=true
          Command with filters and boolean *AND* operator gets satisfying spells.

    *Filters:*

        • level _int_
        • ritual _bool_
        • concentration _bool_

/settings - show user's settings
/help - this help
    """
    #update.message.reply_text(text=help_text, parse_mode=ParseMode.MARKDOWN)
    send_message(context.bot, update.message.chat_id, text=help_text, parse_mode=ParseMode.MARKDOWN)

@overall_logging
def settings(update: Update, context: CallbackContext):
    user_class = context.user_data.get("class")
    if user_class:
        msg = f'Class: {user_class.capitalize()} {replay_for_class(user_class)}'
    else:
        msg = 'No class specified'
    update.message.reply_text(msg)

@overall_logging
def set_class(update: Update, context: CallbackContext):
    # chat_id = update.message.chat_id
    classes = [
        'barbarian', 'bard', 'cleric', 'druid', 'fighter', 'monk', 'paladin',
        'ranger', 'rogue', 'sorcerer', 'warlock', 'wizard']

    # args[0] should contain the class name
    try:
        user_class = context.args[0].lower()
        if user_class not in classes:
            _msg = '\n'.join([f'• {x.capitalize()}' for x in classes])
            update.message.reply_text(f'Wrong class: {user_class}.\n\nAvaliable D&D classes: \n\n{_msg}')
            return
        context.user_data['class'] = user_class.capitalize()
        update.message.reply_text(replay_for_class(user_class))
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /class <your class>')

@overall_logging
def spell_by_name(update: Update, context: CallbackContext):
    """
    /spellbyname <name>
    """
    user_input = context.args
    if user_input:
        user_input = ' '.join([x.capitalize() for x in context.args])
        if(founded_spells := spells.get_spells_by_name(user_input)):
            founded_spells = founded_spells.to_json()
            if len(founded_spells['spells']) == 1:
                update.message.reply_text(print_spell(founded_spells['spells'][0]), parse_mode=ParseMode.MARKDOWN)
            else:
                msg = '\n'.join([f'{magic_wand} *{x["name"]}*' for x in founded_spells['spells']])
                send_message(context.bot, update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text('Nothing found')
    else:
        update.message.reply_text('Usage: /spellbyname <spell name>')

@overall_logging
def spell_search(update: Update, context: CallbackContext):
    """
    /spellsearch [filter1=var1 & filter2 = var2]

    if no filters /spellserach returns all spells for pointed class
    """

    filters = {}
    if (user_class := context.user_data.get("class")):
        filters.update({'classes': user_class})
    
    p = Parser()

    if (user_input := context.args):
        parsed_input = p(' '.join([x for x in user_input]))
        filters.update(parsed_input)

    logger.debug(f'Looking for spells: {filters}')

    founded_spells = spells.get_spells_by(filters)
    logger.debug(f'Founded spells: {founded_spells}')
    if founded_spells:
        founded_spells = founded_spells.to_json()
        msg = '\n'.join([f'{magic_wand} *{x["name"]}*' for x in founded_spells['spells']])
        send_message(context.bot, update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text('Nothing found')

@overall_logging
def error(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error: {context.error}')

@overall_logging
def unknown(update, context):
    update.message.reply_text('What a spell is this? I do not know this type of magic!')

def main():
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', help_msg))
    updater.dispatcher.add_handler(CommandHandler('class', set_class, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('spellbyname', spell_by_name, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('spellsearch', spell_search, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('settings', settings))
    updater.dispatcher.add_handler(CommandHandler('help', help_msg))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
