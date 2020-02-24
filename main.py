import logging
import os
import requests
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN_FILE = 'private_keys/telegram.token'
BASE_API_URL = 'https://api.exchangeratesapi.io'


def get_token(filename):
    if os.path.exists(filename):
        f = open(filename)
        token = f.readline()
        logging.debug('token %s', token)
        f.close()
    else:
        logging.debug('file is not exist')
        token = ''
    return token


# Helper functions
def get_latest_currency_api(url, code):
    prefix_url = '/latest?base='+code
    content = requests.get(url=url+prefix_url).json()
    logger.debug('get latest currency from %s: %s', url, content)
    return content


# End helper functions
# Telegram functions
def start(update, context):
    update.message.reply_text("It is a simple currency convector")


def list(update, context):
    '''
    # /list, /lst returns list of all available rates from: https://api.exchangeratesapi.io/latest?base=USD
    :param update:
    :param contexct:
    :return:
    '''
    currency = get_latest_currency_api(BASE_API_URL, 'USD')
    if not currency:
        update.message.reply_text("list got it")
    else:
        update.message.reply_text("Service has some errors!")
    user = update.message.from_user
    logger.info("User %s start use 'list' command.", user.first_name)


def exchange(update, context):
    '''
    $10 to CAD or  /exchange 10 USD to CAD - converts to the second currency with two decimal precision and return.
    Ex.:  $15.55
    :param update:
    :param context:
    :return:
    '''
    user = update.message.from_user
    logger.info("User %s start use 'exchange' command.", user.first_name)


def history(update, context):
    '''
    USD/CAD for 7 days - return an image graph chart which shows the exchange rate graph/chart
    of the selected currency for the last 7 days
    :param update:
    :param context:
    :return:
    '''
    user = update.message.from_user
    logger.info("User %s start use 'history' command.", user.first_name)


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye!.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# End telegram functions

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = get_token(TOKEN_FILE)
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler(['list', 'lst'], list))
    dp.add_handler(CommandHandler('exchange', exchange))
    dp.add_handler(CommandHandler('history', history))
    dp.add_handler(CommandHandler(['cancel', 'exit', 'quit'], cancel))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
