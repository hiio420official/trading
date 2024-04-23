from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.mysql import TEXT, BIGINT

from app.database import BaseEntity


class StockChartDataRecord(BaseEntity):
    __tablename__ = 'TB_STOCK_CHART_RECORD'

    code = Column("CODE", String(20), ForeignKey("TB_STOCK_CODE.CODE"), primary_key=True)
    minDatetime = Column("MIN_DATE_TIME", BIGINT, nullable=True)
    maxDatetime = Column("MAX_DATE_TIME", BIGINT, nullable=True)
    errorLog = Column("ERROR_LOG", TEXT, nullable=True)
    total = Column("TOTAL", BIGINT, nullable=True)
    regDt = Column("REG_DT", TIMESTAMP, server_default=func.now())
    updtDt = Column("UPDT_DT", TIMESTAMP, onupdate=func.now())
