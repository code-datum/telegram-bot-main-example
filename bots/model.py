import os
from bots.config import *
from urllib.parse import urlencode
import requests

class Currency_exchange_bot_model():
    currencies_type = 'currencies'
    latest_type = 'latest'
    round_index = 5

    def __init__(self, token_path, url_api, round_index, currencies_url):
        # get token to connect with telegram api
        self.token = self.get_token(token_path)
        self.url_api = url_api
        self.round_index = round_index
        self.currencies_url = currencies_url

    def get_token(self, filename):

        if os.path.exists(filename):
            f = open(filename)
            token = f.readline()
            logger.debug('token %s', token)
            f.close()
        else:
            logger.debug('file is not exist')
            token = ''
        return token

    def query_to_api(self, type_query, args):
        content = {}
        if type_query == 'general':
            prefix_url = '/latest?' + urlencode({'base': args['code']})
            content = requests.get(url=self.url_api + prefix_url).json()
        elif type_query == 'history':
            prefix_url = '/history?' + urlencode({'start_at': args['start_at'],
                                                  'end_at': args['end_at'],
                                                  'base': args['base'],
                                                  'symbols': args['symbols']
                                                  })
            content = requests.get(url=self.url_api + prefix_url).json()
        logger.info("query_url's result:{} {}".format(content, type(content)))
        return content

    def exchange(value, from_currency, to_currency='USD'):
        logger.info("test_exchange function is run")
        content = self.get_latest_currency(code=from_currency)
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

    def get_currency_title(self, code):
        '''
        Return by code currencies title
        :return: string
        '''
        # https://openexchangerates.org/api/currencies.json
        currencies_title = self.query_to_api('currencies', self.currencies_type)
        if code in currencies_title:
            return currencies_title[code]
        else:
            return None

    def get_latest_currency(self, from_currency):
        '''
        Get from api the latest currency
        :param from_currency:
        :return:
        '''
        return self.query_to_api('latest', {'code': from_currency})

