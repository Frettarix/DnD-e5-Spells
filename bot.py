import threading
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from setup import TOKEN
# from database import save_to_mongo, DatabaseUnavaliable

from common import createLogger


logger = createLogger(__name__)


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
            # try:
            #     # TODO: implement multithreading for logging
            #     save_result = save_to_mongo(log_info)
            #     logger.info(f'Logs saved: {save_result.inserted_id}')
            #     logger.info(f'function: {handler.__name__}')
            #     logger.info(f'user: {update.effective_user.username}')
            #     logger.info(f'message: {update.message.text}')
            # except DatabaseUnavaliable:
            #     logger.warning(f'Database for logs is unavaliable. Using verbosed console log')
            #     logger.info(log_info)
        return handler(*args, **kwargs)
    return inner

@overall_logging
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        """Hello, adventurer!
        First, use
        /class <your class> -- to set your class
        Next,
        /spells -- to get all the spells of your class
        """
    )

@overall_logging
def set_class(update: Update, context: CallbackContext):
    user_class = update.message.text
    update.message.reply_text(f'You typed: {user_class}')

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

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('class', set_class))
    updater.dispatcher.add_handler(CommandHandler('spells', spells))

    updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
