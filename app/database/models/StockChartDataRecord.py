from sqlalchemy import Column, String, ForeignKey, Integer, TIMESTAMP, func
from sqlalchemy.dialects.mysql import TEXT

from app.database import BaseEntity


class StockChartDataRecord(BaseEntity):
    __tablename__ = 'TB_STOCK_CHART_RECORD'

    code = Column("CODE", String(20), ForeignKey("TB_STOCK_CODE.CODE"), primary_key=True)
    minDate = Column("MIN_DATE", Integer, nullable=True)
    maxDate = Column("MAX_DATE", Integer, nullable=True)
    minTime = Column("MIN_TIME", Integer, nullable=True)
    maxTime = Column("MAX_TIME", Integer, nullable=True)
    errorLog = Column("ERROR_LOG", TEXT, nullable=True)
    total = Column("TOTAL", Integer, nullable=True)
    regDt = Column("REG_DT", TIMESTAMP, server_default=func.now())
    updtDt = Column("UPDT_DT", TIMESTAMP, onupdate=func.now())
