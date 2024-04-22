import asyncio

from sqlalchemy import select, func, and_
from sqlalchemy.dialects.mysql import insert

from .cybos.StockChartData import StockChartData
from threading import Thread
import time
from datetime import datetime
from .database import StockCodeEntity, StockChartEntity
from .database.Core import SessionLocal
from multiprocessing import Pool, cpu_count, Process

from .database.service.CodeService import get_code_name_list, get_min_date


class ThreadWrapper:
    def __init__(self, code_list):
        self.code_list = code_list

    async def run(self):
        start = time.time()
        print(start)
        while self.code_list:
            code = self.code_list.pop(0)
            max_date = datetime.now().strftime('%Y%m%d')

            task = StockChartData(max_date)
            await task(code)


codeList = [c.code for c in get_code_name_list()]


def getDataList(codeList):

    for code in codeList:
        getData(code)

error_code = []
def getData(code):
    global error_code
    max_date = None
    # max_date = get_min_date(code)
    if max_date is None:
        max_date = datetime.now().strftime('%Y%m%d')
    try:
        task = StockChartData(max_date)
        data = task(code)
    except Exception as e:
        print(code,str(e))
        with open(".\\app\\error\\"+code+".txt","w",encoding="utf-8") as f:
            f.write(str(e))





if __name__ == "__main__":
    # procs = []
    #
    # p_list = []
    # size = 12
    # ck = 0
    # for i in range(size):
    #     sp = (len(codeList) // size)
    #     if i == size - 1:
    #         sub_list = codeList[i * sp:]
    #     else:
    #         sub_list = codeList[i * sp:(i + 1) * sp]
    #     ck += len(sub_list)
    #
    #     p = Process(target=getData, args=(sub_list,))
    #     p_list.append(p)
    #
    # print(len(codeList), "-=>", ck)
    # for p in p_list:
    #     p.start()
    #
    with Pool(10) as p:
        p.map(getData, codeList)

    # getData(codeList[0])