from sqlalchemy import select

from .. import StockCodeEntity
from ..Core import SessionLocal

def get_code_name_list():
    with SessionLocal() as session:
        return session.execute(select(StockCodeEntity)).all()