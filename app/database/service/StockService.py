from sqlalchemy import update

from app.database.Core import SessionLocal
from app.database.models.StockChartDataRecord import StockChartDataRecord


def insert_stock_data_record(data):
    with SessionLocal() as session:
        row = session.query(StockChartDataRecord).filter(StockChartDataRecord.code == data["code"]).first()
        if row is None:

            session.add(StockChartDataRecord(**data))
            session.commit()
        else:
            updatedRowCnt = session.execute(
                update(StockChartDataRecord).where(StockChartDataRecord.code == data["code"]).values(**data))
            session.commit()
            print(updatedRowCnt.scalar())
