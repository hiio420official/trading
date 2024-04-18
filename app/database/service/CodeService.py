from sqlalchemy import select, func, text

from .. import StockCodeEntity, StockChartEntity
from ..Core import SessionLocal


def get_code_name_list():
    with SessionLocal() as session:
        return session.query(StockCodeEntity).all()


def get_min_date(code):
    with SessionLocal() as session:
        smpt = select(func.min(StockChartEntity.date)).filter(StockChartEntity.code == code)
        return session.execute(smpt).scalars().first()


def get_daily(code):
    with SessionLocal() as session:
        query = text("""
        SELECT
            A.DATE,
            A.CODE,
            MIN(A.TIME) AS TIME,
            MAX(HIGH) AS HIGH,
            MIN(LOW) AS LOW,
            SUM(VOLUME) AS VOLUME,
            (SELECT Z.CLOSE FROM TB_STOCK_CHART Z WHERE Z.DATE = A.DATE AND A.CODE = Z.CODE AND Z.TIME = MAX(A.TIME)) AS CLOSE,
            (SELECT Z.OPEN FROM TB_STOCK_CHART Z WHERE Z.DATE = A.DATE AND A.CODE = Z.CODE AND Z.TIME = MIN(A.TIME)) AS OPEN
        FROM TB_STOCK_CHART A
        WHERE
            A.CODE =:stock_code
        GROUP BY A.DATE,A.CODE;
        """)
        params = {'stock_code': code}
        # Execute the query and fetch the results
        results = session.query(StockChartEntity).from_statement(query).params(**params).all()
        print(results[0].__dict__)
    return None


if __name__ == "__main__":
    get_daily("A000020")
