# the task https://docs.google.com/document/d/1_UNymiQ0otjI9RBeW7-pwDdgQUW_OveUlcet01zzIsM/edit?usp=sharing

import os
import requests
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from urllib.parse import urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import *
from .model import Currency_exchange_bot_model as Model


class Currency_exchange_bot(Model):
    # Helper functions
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
