from collections import OrderedDict

from sqlalchemy import text

from app.database import StockChartEntity
from app.database.Core import SessionLocal, engine
import numpy as np
import pandas as pd
from PIL import Image

# h,w
# x = np.zeros((800, 1024, 3), dtype=np.uint8)  # PIL image to NumPy array
# x+=255
# x[150:200,150:200] = np.ones((3));
#
# print(x)
#
# img_2 = Image.fromarray(x,"RGB")  # NumPy array to PIL image
# img_2.show()


class Scaler:
    def __init__(self, range_list, domain_list):
        self.ri = range_list[0]
        self.ro = range_list[1]
        self.di = domain_list[0]
        self.do = domain_list[1]

    def __call__(self, value):
        return self.ro - (self.do - value ) / (self.do - self.di) * (self.ro - self.ri)


if __name__ == "__main__":
    with engine.connect() as conn, conn.begin():
        stmt = text("""SELECT 
                *
                FROM 
                TB_STOCK_CHART 
                WHERE CODE = :code 
                ORDER BY DATE ASC , TIME ASC 
                LIMIT 0,300
                """)
        params = {"code": "A000020"}
        df = pd.read_sql_query(stmt, con=conn, params=params)
        df["DATETIME"] = df["DATE"].astype("str") + df["TIME"].apply(lambda x: str(x).zfill(4))

        df_c = df.drop(["CODE", "DATE", "TIME"], axis=1)
        df_c["MA5"] = df_c['CLOSE'].rolling(window=5).mean()
        df_c.fillna(0, inplace=True)
        scaler = Scaler([800, 0], [df_c[["CLOSE", "OPEN", "LOW", "HIGH"]].min().min(),
                                   df_c[["CLOSE", "OPEN", "LOW", "HIGH"]].max().max()])
        df_sc = df_c[["CLOSE", "OPEN", "LOW", "HIGH"]].apply(scaler,axis=1).astype("int")

        print(df_sc.shape)
        df_sc["width"] = 900//df_sc.shape[0]
        df_sc["x"] = df_sc.index * df_sc["width"]

        print(df_sc)