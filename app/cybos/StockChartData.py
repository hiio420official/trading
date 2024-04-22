import win32com.client
from sqlalchemy import select, and_
from sqlalchemy.dialects.mysql import insert

from .Cybos import Cybos
from ..database.Core import SessionLocal
from ..database.models.StockData import StockChartEntity


class StockChartData(Cybos):
    """

    https://money2.daishin.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=102&page=1&searchString=StockChart&p=8839&v=8642&m=9508
    """

    def __init__(self, max_date="20240413", min_date="19770101"):
        super().__init__()
        self.obj = win32com.client.Dispatch("CpSysDib.StockChart")

        self.var = var
        self.keys = list(self.var.keys())

        self.obj.SetInputValue(1, ord('1'))  # 기간으로 받기
        self.obj.SetInputValue(2, max_date)  # To 날짜
        self.obj.SetInputValue(3, min_date)  # From 날짜
        # self.obj.SetInputValue(4, 500)  # 최근 500일치
        print(max_date, min_date)
        self.obj.SetInputValue(5, self.keys)  # 날짜,시가,고가,저가,종가,거래량
        self.obj.SetInputValue(6, ord('m'))  # '차트 주기 - 일간 차트 요청
        self.obj.SetInputValue(7, 1)  # '차트 주기 - 일간 차트 요청

        self.obj.SetInputValue(9, ord('1'))  # 수정주가 사용

    def __call__(self, code):
        self.obj.SetInputValue(0, code)  # 종목코드
        rqStatus = self.obj.GetDibStatus()
        rqRet = self.obj.GetDibMsg1()
        data = self.get()
        self._save(data)
        print(self.obj.GetHeaderValue(6),self.obj.GetHeaderValue(5),self.obj.GetHeaderValue(7))
        print(code, " ===>len", self.obj.GetHeaderValue(3), len(data), data[-1]["date"], data[0]["date"], "\r", end="")
        while self.obj.Continue:
            self.obj.BlockRequest()
            next_data = self.get()
            self._save(next_data)
            data += next_data
            print(code, " ===>len", self.obj.GetHeaderValue(3), len(data), data[-1]["date"], data[0]["date"], "\r",end="")

        return data

    def get(self):
        self.obj.BlockRequest()
        rn = range(len(self.keys))
        data = []
        for idx in range(self.obj.GetHeaderValue(3)):
            item = {"code": self.obj.GetHeaderValue(0)}
            for rnx in rn:
                key = self.var[self.keys[rnx]]
                value = self.obj.GetDataValue(rnx, idx)
                item[key] = value
            data.append(item)
        return data

    def _save_dup(self, data):
        with SessionLocal() as session:
            insert_stmt = insert(StockChartEntity).values(data)
            update_dict = {x.name: x for x in insert_stmt.inserted}
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**update_dict)
            session.execute(on_duplicate_key_stmt)
            session.commit()

    def _save(self,data_list):
        with SessionLocal() as session:
            i = 0
            for data in data_list:
                result = session.query(StockChartEntity).filter(and_(StockChartEntity.code == data["code"], StockChartEntity.date==data["date"], StockChartEntity.time==data["time"])).all()
                if len(result) == 0:
                    session.add(StockChartEntity(**data))
                    session.commit()
                    i+=1
            print(len(data_list), " ===>len", i, "\r",end="")
var = {
    "0": "date",
    "1": "time",
    "2": "open",
    "3": "high",
    "4": "low",
    "5": "close",
    "6": "comparedToThePreviousDay",
    "8": "volume",
    "9": "tradingValue",
    "10": "cumulativeSoldQuantity",
    "11": "cumulativeTransactionQuantity",
    "12": "numberOfListedStocks",
    "13": "marketCapitalization",
    "14": "foreignOrderLimitQuantity",
    "15": "quantityAvailableForForeignersToOrder",
    "16": "foreignersCurrentHoldings",
    "17": "foreignCurrentHoldingRatio",
    "18": "dateOfRevisedStockPrice",
    "19": "modifiedStockPriceRatio",
    "20": "institutionalNetPurchaseVolume",
    "21": "cumulativeInstitutionalNetPurchaseVolume",
    "22": "arrangementForArrivalAndDeparture",
    "23": "fluctuatingRate",
    "24": "deposit",
    "25": "stockTurnover",
    "26": "transactionCompletionRate",
    "37": "contrastMark",
    "62": "executionPriceComparisonTransactionSaleQuantity",
    "63": "executionPriceComparisonTransactionQuantity"
}

# 2 ('날짜', '시간', '시가', '고가', '저가', '종가', '전일대비', '거래량', '거래대금', '누적체결매도수량', '누적체결매수수량', '상장주식수', '시가총액', '외국인주문한도수량', '외국인주문가능수량', '외국인현보유수량', '외국인현보유비율', '수정주가일자', '수정주가비율', '기관순매수량', '기관누적순매수량', '등락주선', '등락비율', '예탁금', '주식회전율', '거래성립률', '대비부호', '체결가비교체결매도수량', '체결가비교체결매수수량')
