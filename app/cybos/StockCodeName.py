import win32com.client
from sqlalchemy.dialects.mysql import insert

from .Cybos import Cybos
from ..database.Core import SessionLocal
from ..database.models.StockCode import StockCodeEntity


class StockCodeName(Cybos):

    def __init__(self):
        super().__init__()

    def get(self):
        if not self.connected():
            print("self.stockConn.conn", self.connected())
            return
        else:
            print("접속중")
        # 종목코드 리스트 구하기
        objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        codeList = objCpCodeMgr.GetStockListByMarket(1)  # 거래소
        codeList2 = objCpCodeMgr.GetStockListByMarket(2)  # 코스닥
        data = []

        data += [{"type": "KOSPI", "code": code, "name": objCpCodeMgr.CodeToName(code),
                  "second_code": objCpCodeMgr.GetStockSectionKind(code)} for code in codeList]
        data += [{"type": "KOSDAQ", "code": code, "name": objCpCodeMgr.CodeToName(code),
                  "second_code": objCpCodeMgr.GetStockSectionKind(code)} for code in codeList2]
        return data

    def save(self, data):
        with SessionLocal() as session:
            insert_stmt = insert(StockCodeEntity).values(data)
            update_dict = {x.name: x for x in insert_stmt.inserted}
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**update_dict)
            session.execute(on_duplicate_key_stmt)
            session.commit()
