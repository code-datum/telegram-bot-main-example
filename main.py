# 1 Import the libraries
from telegram.ext import Updater, CommandHandler
import requests
import logging
import os

logging.basicConfig(level=logging.DEBUG)
import re

TOKEN_FILE = 'private_keys/RandomDogExBot.token'


# 2 Asses the API andd get the image URL
# {"fileSizeBytes":104652,"url":"https://random.dog/5c9f8baf-7918-4545-bd86-8f441cf96f3e.jpg"}
# contents = requests.get('https://random.dog/woof.json').json()
# image_url = contents['url']
# logging.debug("image_url%s ", image_url)

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


def get_url():
    '''
    get the image URL
    :return string:
    '''
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    logging.debug("image_url%s %s ", url, 'get_url')
    return url


def bop(bot, update):
    '''
    # 3 send the image
    :param bot:
    :param update:
    :return void:
    '''
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def main():
    TOKEN = get_token(TOKEN_FILE)
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
