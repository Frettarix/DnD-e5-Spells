import threading
from telegram import Bot, Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from setup import TOKEN
# from database import save_to_mongo, DatabaseUnavaliable

from common import createLogger


logger = createLogger(__name__)


def overall_logging(handler):
    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message') and hasattr(update, 'effective_user'):
            log_info = f'handler: {handler.__name__}, message: "{update.message.text}", user: {update.effective_user.username}'
            logger.info(log_info)
        return handler(*args, **kwargs)
    return inner

# @overall_logging
# def start(update: Update, context: CallbackContext):
#     """Send a message when the command /start is issued."""
#     update.message.reply_text(
#     """
#     Hello, adventurer!
# First, use
# /class <your class> -- set your class
# Next,
# /spells -- to get all the spells of your class
# """
#     )

@overall_logging
def help_msg(update: Update, context: CallbackContext):
    help_text = """/class <your class> - set your class
/spells _optional filters_

    *Query examples:*

        • /spells
          Command without arguments gets all the spells of your class. If no class specified all the spells shows.

        • /spells "acid arrow"
          Command with spell name in double brackets gets the spell description if it exists.

        • /spells level=2 & ritual=true | concentration=true
          Command with filters and boolean operators *AND/OR* gets satisfying spells.

    *Filters:*

        • level _int_
        • ritual _bool_
        • concentration _bool_

/settings - show user's settings
/help - this help
    """
    update.message.reply_text(text=help_text, parse_mode=ParseMode.MARKDOWN)

@overall_logging
def settings(update: Update, context: CallbackContext):
    update.message.reply_text(
        f'Class: {context.user_data["class"]}'
    )

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
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /class <your class>')

    context.user_data['class'] = user_class

@overall_logging
def spells(update: Update, context: CallbackContext):
    update.message.reply_text('Under construction')

# @overall_logging
# def echo(update: Update, context: CallbackContext):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)

@overall_logging
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', help_msg))
    updater.dispatcher.add_handler(CommandHandler('class', set_class, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('spells', spells))
    updater.dispatcher.add_handler(CommandHandler('settings', settings))
    updater.dispatcher.add_handler(CommandHandler('help', help_msg))

    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
