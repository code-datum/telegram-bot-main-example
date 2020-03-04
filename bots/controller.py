# the task https://docs.google.com/document/d/1_UNymiQ0otjI9RBeW7-pwDdgQUW_OveUlcet01zzIsM/edit?usp=sharing

import os
import sys
import requests
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from urllib.parse import urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bots.config import *
from bots.model import Currency_exchange_bot_model as Model

logging.basicConfig(filename='debug.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
import datetime as date


class Currency_exchange_bot(Model):
    debug = False

    # Helper functions
    # End helper functions
    # Telegram functions
    def __init__(self, token_path, debug=False):
        self.debug = debug
        super().__init__(token_path=token_path,
                         round_index=round_index,
                         url_api=base_api_url,
                         currencies_url=currencies_url)

    def start(self, update, context):
        update.message.reply_text("It is a simple currency convector")

    def list(self, update, context):

        '''
        # /list, /lst returns list of all available rates from: https://api.exchangeratesapi.io/latest?base=USD
        :param update:
        :param contexct:
        :return:
        '''

        if update:
            currency = get_latest_currency('USD')
            if currency:
                update.message.reply_text("Currency now:"
                                          "{}".format(currency['rates']))
            else:
                update.message.reply_text("Service has some errors!")
                user = update.message.from_user
                logger.info("User %s start use 'list' command.", user.first_name)
        else:
            # there is a flask view area
            logger.info("Debug mode list started")

    def exchange(self, update, context):
        '''
        $10 to CAD or  /exchange 10 USD to CAD - converts to the second currency with two decimal precision and return.
        Ex.:  $15.55
        :param update:
        :param context:
        :return:
        '''

        if update:
            user = update.message.from_user
            logger.info("User %s start use 'exchange' command.", user.first_name)
        else:
            # there is a flask view area
            logger.info("Debug mode exchange started")

    def history(self, update, context):
        '''
        USD/CAD for 7 days - return an image graph chart which shows the exchange rate graph/chart
        of the selected currency for the last 7 days
        :param update:
        :param context:
        :return:
        # prepare data to telegram api
        '''
        # tday is today
        tday = date.date.today()
        # get tha last 7 days
        differ_day = 7
        tdelta = date.timedelta(days=differ_day)
        differ_date = tday - tdelta
        from_currency = "CAD"
        converted_currency = "USD"
        map = {
            'start_at': differ_date,
            'end_at': tday,
            'base': converted_currency,
            'symbols': from_currency
        }
        content = self.query_to_api('history', map)

        # content = logger.info("history %s", content['rates'])

        if 'rates' in content:
            rates = content['rates']

            rates_keys = [i for i in rates]
            rates_values = [v[from_currency] for k, v in rates.items()]

            logger.info("rates_key {}".format(rates_keys))
            logger.info("rates_values {}".format(rates_values))
        else:
            logger.info("Content has not %s", content['rates'])
        ## TODO make a picture from url
        # telegram-bot api
        if update:
            user = update.message.from_user
            chat_id = update.message.chat_id
            logger.info("User %s start use 'history' command.", user.first_name)
            update.message.reply_text("The graph from {} to {}".format(differ_date, tday))
            context.bot.send_photo(chat_id=chat_id, photo=open('bots/static/image/2020-03-03-17_45_23.png', 'rb'))
            # bot.send_photo(chat_id, photo=self.get_url())
        # a test block
        else:
            logger.info("Debug mode history started")

        return content

    def get_url():
        '''
        get the image URL
        :return string:
        '''
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
        logging.debug("image_url%s %s ", url, 'get_url')
        return url

    def cancel(self, update, context):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye!.',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def run(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary

        if not self.debug:
            updater = Updater(self.token, use_context=True)

            # Get the dispatcher to register handlers
            dp = updater.dispatcher

            dp.add_handler(CommandHandler('start', self.start))
            dp.add_handler(CommandHandler(['list', 'lst'], self.list))
            dp.add_handler(CommandHandler('exchange', self.exchange))
            dp.add_handler(CommandHandler('history', self.history))
            dp.add_handler(CommandHandler(['cancel', 'exit', 'quit'], self.cancel))

            # log all errors
            dp.add_error_handler(self.error)

            # Start the Bot
            updater.start_polling()

            # Run the bot until you press Ctrl-C or the process receives SIGINT,
            # SIGTERM or SIGABRT. This should be used most of the time, since
            # start_polling() is non-blocking and will stop the bot gracefully.
            updater.idle()

    def test_run(self):
        # run test mode
        self.history(update=None, context=None)
