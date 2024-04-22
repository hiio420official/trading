from sqlalchemy import Column, String

from ..Core import BaseEntity


class StockCodeEntity(BaseEntity):
    __tablename__ = 'TB_STOCK_CODE'

    code = Column("CODE", String(20), primary_key=True)
    name = Column("NAME", String(256))
    second_code = Column("SECOND_CODE", String(20))
    type = Column("TYPE", String(6))
