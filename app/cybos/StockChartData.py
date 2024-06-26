import win32com.client
from sqlalchemy import and_
from sqlalchemy.dialects.mysql import insert

from .Cybos import Cybos
from ..database.Core import SessionLocal
from ..database.models.StockData import StockChartEntity
from ..database.service.StockService import insert_stock_data_record, select_stock_data_record, \
    update_stock_data_record, select_stock_data, insert_stock_data


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
        if max_date != "":
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
        data = self.get(code)
        print(code, "\tfirst\t", len(data))
        while self.obj.Continue:
            next_data = self.get(code)

            data += next_data
            print(code, "\tContinue\t", len(data))
        if len(data) > 0:
            print(code, " ===>len", self.obj.GetHeaderValue(3), len(data), data[-1]["date"], data[0]["date"])
        self._save(data)
        return data

    def get(self,code):
        self.obj.BlockRequest()
        rn = range(len(self.keys))
        data = []
        for idx in range(self.obj.GetHeaderValue(3)):
            item = {"code":code}
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

    def _save(self, data_list):
        i = 0
        code = ""
        max_dt = 0
        min_dt = 99999999999999
        for data in data_list:
            if data["code"] != "":
                code = data["code"]
            date = data["date"]
            time = data["time"]
            dt = int(str(date) + str(time).zfill(2))
            if dt > max_dt:
                max_dt = dt
            if dt < min_dt:
                min_dt = dt
            result = select_stock_data(data)
            if len(result) == 0:
                insert_stock_data(data)
                i += 1
        if code != "":
            data = {"code": code, "minDatetime": min_dt, "maxDatetime": max_dt}
            row = select_stock_data_record(code)
            if row is None:
                insert_stock_data_record(data)
            else:
                if max_dt > row.maxDatetime:
                    update_stock_data_record({"code": code, "maxDatetime": max_dt})
                if min_dt < row.minDatetime:
                    update_stock_data_record({"code": code, "minDatetime": min_dt})
            print(min_dt, max_dt, " ===>len", i, "\r", end="")


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
