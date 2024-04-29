from sqlalchemy import update, and_

from app.database import StockChartEntity
from app.database.Core import SessionLocal
from app.database.models.StockChartDataRecord import StockChartDataRecord



def select_stock_data_record(code):
    with SessionLocal() as session:
        return session.query(StockChartDataRecord).filter(StockChartDataRecord.code == code).first()

def insert_stock_data_record(data):
    with SessionLocal() as session:
        session.add(StockChartDataRecord(**data))
        session.commit()

def update_stock_data_record(data):
    with SessionLocal() as session:
        updated_row_cnt = session.execute(
            update(StockChartDataRecord).where(StockChartDataRecord.code == data["code"]).values(**data))
        session.commit()
        print(updated_row_cnt.rowcount)


def select_stock_data(data):
    with SessionLocal() as session:
        return session.query(StockChartEntity).filter(
                        and_(StockChartEntity.code == data["code"], StockChartEntity.date == data["date"],
                             StockChartEntity.time == data["time"])).all()

def insert_stock_data(data):
    with SessionLocal() as session:
        session.add(StockChartEntity(**data))
        session.commit()

