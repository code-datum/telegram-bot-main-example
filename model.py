from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Currencies, Rates
import json
engine = create_engine('sqlite:///local.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_rates(rates):
    '''
    add rates to local db
    :param rates: dict
    :return void:
    '''
    rates_json = json.dumps(rates)
    rates_model = Rates(rates=rates_json)
    session.add(rates_model)
    session.commit()
    DbRates = session.flush()
    return DbRates


def add_currencies(currency, rates_id):
    currencies_model = Currencies(
        base=currency['base'],
        date=currency['date'],
        rates_id=Rates.id,
    )
    session.add(currencies_model)
    session.commit()
    # return currency_id
