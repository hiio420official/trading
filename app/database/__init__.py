import logging
import sqlparse

from .Core import BaseEntity, engine
from .models.StockCode import StockCodeEntity
from .models.StockData import StockChartEntity
from .models.StockChartDataRecord import StockChartDataRecord

__all__ = ["StockCodeEntity", "StockChartEntity", "StockChartDataRecord", "BaseEntity", "engine"]
BaseEntity.metadata.create_all(bind=engine)


class SqlFormatter(logging.Formatter):
    def format(self, record):
        sql = sqlparse.format(
            record.getMessage(),
            keyword_case="upper",
            identifier_case="lower",
            truncate_strings=50,
            reindent=True
        ).strip('')
        sql = '\n\t\t '.join([l for l in sql.split('\n')])
        return sql


sql_logging = logging.getLogger("sqlalchemy.engine.Engine")
sql_logging.setLevel("DEBUG")
handler = logging.StreamHandler()
handler.setFormatter(SqlFormatter())

sql_logging.addHandler(handler)

