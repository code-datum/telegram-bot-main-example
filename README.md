# telegram-bot-main-example
the tutor get from https://www.freecodecamp.org/news/learn-to-build-your-first-bot-in-telegram-with-python-4c99526765e4/

Url adress bot: https://telegram.me/RandomDogExamBot

## Create a new bot

Go to the Botfather [https://telegram.me/BotFather] and send new command '/newbot' command.
get a token for your bot

```python
'704418931:AAEtcZ*************'
```

create venv and activate
```bash
virtualenv venv
source venv/bin/activate

```
install telegram bot package

```bash
echo 'python-telegram-bot' >> requirements.txt
```
##1. Import the libraries

```python
from telegram.ext import Updater, CommandHandler
import requests
import re
``` 

Main template code to initialize bot 
```python
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

```