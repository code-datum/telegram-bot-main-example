# the task https://docs.google.com/document/d/1_UNymiQ0otjI9RBeW7-pwDdgQUW_OveUlcet01zzIsM/edit?usp=sharing

import os
import requests
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from urllib.parse import urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bots.config import *
from bots.model import Currency_exchange_bot_model as Model

from datetime import date


class Currency_exchange_bot(Model):
    debug = False

    # Helper functions
    # End helper functions
    # Telegram functions
    def __init__(self, token_path, debug):
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
        '''
        if update:
            user = update.message.from_user
            logger.info("User %s start use 'history' command.", user.first_name)
        else:
            #there is a flask view area
            logger.info("Debug mode history started")

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


