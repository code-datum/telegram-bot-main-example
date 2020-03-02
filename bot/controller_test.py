from bot.config import *
from bot.model import Currency_exchange_bot_model as Model

class Currency_exchange_bot(Model):

    def __init__(self, token_path):
        super().__init__(token_path=token_path)