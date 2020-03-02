# the task https://docs.google.com/document/d/1_UNymiQ0otjI9RBeW7-pwDdgQUW_OveUlcet01zzIsM/edit?usp=sharing
import logging
import os
import requests
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from urllib.parse import urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import *

project_dir = os.path.dirname(os.path.abspath(__file__))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN_FILE = 'private_keys/telegram.token'
BASE_API_URL = 'https://api.exchangeratesapi.io'
DECIMAL_KEY = 2


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
    '''
    return from api row currency by code
    :param url:
    :param code:
    :return type of dict:
    '''
    content = {}
    # logger.info('get latest currency from {}'.format(content))
    # for key, value in content['rates'].items():
    #     content['rates'][key] = round(value, DECIMAL_KEY)
    return content


def get_local_currency():
    pass


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
    if currency:
        update.message.reply_text("Currency now:"
                                  "{}".format(currency['rates']))

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


def test_list():
    logger.info("test_list function is run")
    content = get_latest_currency_api(url=BASE_API_URL, code='CAD')
    logger.info(content)
    for key, value in content['rates'].items():
        print(key, ':', value)
    print('formatted currency {}'.format(content['rates']))
    logger.info("test_list function is end")


def test_exchange(value, from_currency, to_currency='USD'):
    logger.info("test_exchange function is run")
    content = get_latest_currency_api(url=BASE_API_URL, code=from_currency)
    from_currency_unit = content['rates'][to_currency]

    if type(value) is str:
        split_value = value.split('$')
        logger.info(split_value)
        if len(split_value) == 2:
            logger.info('{}'.format(float(split_value[0])))
            converted_money = round(float(split_value[0]) * from_currency_unit, DECIMAL_KEY)
        else:
            converted_money = 0
            logger.error('enter incorrect data')
    elif type(value) is float or type(value) is int:
        converted_money = round(value * from_currency_unit, DECIMAL_KEY)
    else:
        logger.error('enter incorrect data')
        converted_money = 0
    logger.info("converted currency: %s", converted_money)
    logger.info("test_exchange function is run")


def query_to_api(type_query, args):
    if type_query == 'general':
        prefix_url = '/latest?' + urlencode({'base': args['code']})
        content = requests.get(url=BASE_API_URL + prefix_url).json()
    elif type_query == 'history':
        prefix_url = '/history?' + urlencode({'start_at': args['start_at'],
                                              'end_at': args['end_at'],
                                              'base': args['base'],
                                              'symbols': args['symbols']
                                              })
        content = requests.get(url=BASE_API_URL + prefix_url).json()
    logger.info("query_url's result:{}".format(content))
    return content


def test_history():
    logger.info("test_history function is run")
    # query_history = {'start_at': '2019-11-27',
    #          'end_at': '2019-12-03',
    #          'base': 'USD',
    #          'symbols': 'CAD'
    #          }
    # query_general = {
    #     'code':'USD'
    # }
    query_to_api('general', query_general)
    pass
    logger.info("test_history function is run")


# End telegram functions
def test_main():
    # test_list()
    # TODO if value is x$ then auto choose converted type
    # test_exchange('1.25$', 'CAD', 'USD')
    test_history()


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
    # main()
    test_main()
