import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Rates(Base):
    __tablename__ = 'rates'
    id = Column(Integer, primary_key=True)
    rates = Column(String(250), nullable=False)


class Currencies(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    base = Column(String(255), nullable=False)
    date = Column(String(110), nullable=False)
    rates_id = Column(Integer, ForeignKey('rates.id'))
    rates = relationship(Rates)

    # serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'id': self.id,
            'base': self.base,
            'date': self.date,
            'rates_id': self.id
        }


engine = create_engine('sqlite:///local.db')

Base.metadata.create_all(engine)
