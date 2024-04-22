from collections import OrderedDict
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from sqlalchemy import URL

import os

load_dotenv()
url = URL.create(drivername=os.getenv("DB_DRIVERCLASS"), username=os.getenv("DB_USER"),
                 password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"),
                 port=os.getenv("DB_PORT"), database=os.getenv("DB_NAME"))

engine = create_engine(url, pool_recycle=3600, max_overflow=20, pool_size=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseEntity(DeclarativeBase):

    def dict(self):
        return OrderedDict(sorted(self.__dict__.items(), key=lambda x: x[0]))
    pass



