import time
from threading import Thread
import win32com.client
import pythoncom
import inspect

from sqlalchemy import select
from sqlalchemy.sql.expression import func
from app.cybos.Cybos import Cybos
from app.database.Core import SessionLocal
from app.database.models.StockCode import StockCodeEntity


class GetStockData(Cybos):
    """

    https://money2.daishin.com/e5/mboard/ptype_basic/HTS_Plus_Helper/DW_Basic_Read_Page.aspx?boardseq=284&seq=102&page=1&searchString=StockChart&p=8839&v=8642&m=9508
    """

    def __init__(self, code):
        super().__init__()
        self.obj = win32com.client.Dispatch("CpSysDib.StockChart")
        self.code = code
        self.obj.SetInputValue(0, self.code)  # 종목코드
        self.obj.SetInputValue(1, ord('1'))  # 기간으로 받기
        self.obj.SetInputValue(2, "20240413")  # To 날짜
        self.obj.SetInputValue(3, "19770101")  # From 날짜
        # self.obj.SetInputValue(4, 500)  # 최근 500일치
        self.obj.SetInputValue(5,
                               [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                23, 24, 25, 26, 37, 62, 63])  # 날짜,시가,고가,저가,종가,거래량
        self.obj.SetInputValue(6, ord('D'))  # '차트 주기 - 일간 차트 요청
        self.obj.SetInputValue(7, 1)  # '차트 주기 - 일간 차트 요청

        self.obj.SetInputValue(9, ord('1'))  # 수정주가 사용

    def __call__(self):
        self.obj.BlockRequest()
        rqStatus = self.obj.GetDibStatus()
        rqRet = self.obj.GetDibMsg1()
        # for i in range(19):

        data = []
        for i in range(self.obj.GetHeaderValue(3)):
            data.append(self.obj.GetDataValue(2, i))
        print(self.code, " ===>len", self.obj.GetHeaderValue(3), len(data), "\n")

        while self.obj.Continue:
            self.obj.BlockRequest()
            print(self.code, " ===>len", self.obj.GetHeaderValue(3), len(data), "\n")
            for i in range(self.obj.GetHeaderValue(3)):
                data.append(self.obj.GetDataValue(2, i))


class ThreadWrapper(Thread):
    def __init__(self, code_list):
        Thread.__init__(self)
        self.code_list = code_list

    def run(self):
        start = time.time()
        print(start)
        while li:
            code = li.pop(0)
            t = GetStockData(code)
            end = time.time() - start
            t()
            # if end < 1 / 5:
            #     li.append(code)
            # else:
            #
            #     print(t.obj.Continue, end, ">")
            #
            #     start = time.time()


if __name__ == '__main__':
    with SessionLocal() as session:
        c = session.query(func.min(StockCodeEntity.code), func.min(StockCodeEntity.name))
        li = session.execute(select(StockCodeEntity).limit(300)).all()

        li = [la[0].code for la in li]
        size = 30

        thread_list = []
        for i in range(size):
            if i == size - 1:
                c = li[i * size:]
            else:
                c = li[i * size:(i + 1) * size]

            thread_list.append(ThreadWrapper(c))
            print(c)
        for t in thread_list:
            t.start()
