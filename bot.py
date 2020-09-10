from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler
import random
import time
import json
from textwrap import dedent

from setup import TOKEN
from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler
# from database import save_to_mongo, DatabaseUnavaliable

from common import createLogger
from dnd_spells import Parser, Spells, Spell, Normalizer, CantParse


logger = createLogger(__name__)
with open('class_icons.json', 'r') as class_icons_file:
    class_icons = json.load(class_icons_file)
spells = Spells()
norm = Normalizer()

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

def detailed_spell(spell: Spell):
    msg = '\n'.join(line.lstrip() for line in f"""{spell.str_nice()}

        {spell.desc}

        class: {', '.join([x for x in spell.classes])}
        subclass: {', '.join([x for x in spell.subclass])}
        school: {spell.school}""".split('\n'))

    spell_json = spell.to_json()
    for field in spell_json:
        if field not in ['name', 'classes', 'subclass', 'school', 'desc', 'url', 'index']:
            _val = spell_json[field]
            if _val:
                if isinstance(_val, list):
                    _val = ', '.join([x for x in _val])
                msg += f'{field.replace("_", " ")}: {_val}\n'
    return msg

def replay_for_class(user_class):
    user_class = norm(user_class)
    return random.choice(class_icons.get(user_class, class_icons['default']))

@overall_logging
def help_msg(update: Update, context: CallbackContext):
    help_text = """
                /class [class]

                    *Examples:*

                        • /class
                        Reset saved class

                        • /class warlock
                        Set class Warlock

                /spellnamed <spell name>

                    *Examples:*

                        • /spellnamed acid arrow
                        Return Acid Arrow full description

                        • /spellnamed acid
                        Return links to all the spells with 'acid' in name

                /spellsearch [filters]

                    *Examples:*

                        • /spellsearch
                        Return all spells for your class if specified or all spells

                        • /spellsearch level=2 & ritual=true
                        Command with filters and boolean *AND* operator gets satisfying spells.

                    *Filters:*

                        • level _int_
                        • ritual _bool_
                        • concentration _bool_

                /settings - show user's settings

                /help - this help
                """
    send_message(context.bot, update.message.chat_id, text=dedent(help_text), parse_mode=ParseMode.MARKDOWN)

@overall_logging
def settings(update: Update, context: CallbackContext):
    user_class = context.user_data.get("class")
    if user_class:
        msg = f'Class: {user_class} {replay_for_class(user_class)}'
    else:
        msg = 'No class specified'
    update.message.reply_text(msg)

@overall_logging
def set_class(update: Update, context: CallbackContext):
    """
    /class [class]
    """
    classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin',
        'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']

    try:
        user_class = norm(context.args[0])
        if user_class not in norm(classes):
            _msg = '\n'.join([f'• {x}' for x in classes])
            update.message.reply_text(f'Wrong class: {user_class}.\n\nAvaliable D&D classes: \n\n{_msg}')
            return
        context.user_data['class'] = user_class.capitalize()
        update.message.reply_text(replay_for_class(user_class))
    except (IndexError, ValueError):
        context.user_data["class"] = None
        update.message.reply_text('No class specified\nTo set a class: /class <your class>')

@overall_logging
def spell_by_name(update: Update, context: CallbackContext):
    """
    /spellnamed <name>
    """
    user_input = context.args
    if user_input:
        user_input = ' '.join([arg for arg in context.args])
        if(found_spells := spells.get_spells_by_name(user_input)):
            if len(found_spells) == 1:
                update.message.reply_text(detailed_spell(found_spells.spells[0]), parse_mode=ParseMode.MARKDOWN)
            else:
                keyboard = []
                for spell in found_spells:
                    keyboard.append([InlineKeyboardButton(f'{spell.str_nice()}', callback_data=spell.name)])
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Founded spells:', reply_markup=reply_markup)
        else:
            update.message.reply_text('Nothing found')
    else:
        update.message.reply_text('Usage: /spellnamed <spell name>')

@overall_logging
def spell_search(update: Update, context: CallbackContext):
    """
    /spellsearch [filter1=var1 & filter2 = var2]
    if no filters /spellsearch returns all spells for pointed class
    """

    filters = {}
    if (user_class := context.user_data.get("class")):
        filters.update({'classes': user_class})
    
    p = Parser()

    if (user_input := context.args):
        try:
            parsed_input = p(' '.join([x for x in user_input]))
            filters.update(parsed_input)
        except CantParse:
            update.message.reply_text('Wrong filter to search')
            return

    logger.debug(f'Looking for spells: {filters}')

    found_spells = spells.get_spells_by(filters)
    logger.debug(f'Founded spells: {", ".join([x for x in found_spells])}')
    if found_spells:
        found_spells_to_inline = {f'{spell.str_nice()}': spell.name for spell in found_spells}
        context.chat_data['chat_id'] = update.message.chat_id
        send_message_with_inline(context, 'Found spells:', found_spells_to_inline)
    else:
        update.message.reply_text('Nothing found')

@overall_logging
def error(update: Update, context: CallbackContext):
    logger.warning(f'Update {update} caused error: {context.error}')

@overall_logging
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text('What a spell is this? I do not know this type of magic!')

# TODO: rewrite it
def send_message_with_inline(context, msg, inline_buttons: dict, remains_msg='...'):
    context.chat_data['remains'] = None
    context.chat_data['remains_msg'] = None

    if len(inline_buttons) <= 100:
        send_options = inline_buttons
        remain_options = None
    else:
        send_options = dict(list(inline_buttons.items())[:99])
        remain_options = dict(list(inline_buttons.items())[99:])

    keyboard = []
    for name, data in send_options.items():
        keyboard.append([InlineKeyboardButton(name, callback_data=data)])
    if remain_options:
        context.chat_data['remains'] = remain_options
        context.chat_data['remains_msg'] = msg
        keyboard.append([InlineKeyboardButton(remains_msg, callback_data='IN_PROGRESS')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    send_message(context.bot, context.chat_data['chat_id'], msg, reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data != 'IN_PROGRESS':
        spell = spells.get_spells_by_name(query.data).spells[0]
        query.edit_message_text(text=detailed_spell(spell), parse_mode=ParseMode.MARKDOWN)
    else:
        send_message_with_inline(context, context.chat_data['remains_msg'], context.chat_data['remains'])


def main():
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', help_msg))
    updater.dispatcher.add_handler(CommandHandler('class', set_class, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('spellnamed', spell_by_name, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('spellsearch', spell_search, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('settings', settings))
    updater.dispatcher.add_handler(CommandHandler('help', help_msg))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
