import asyncio

from sqlalchemy import select, func, and_

from .cybos.StockChartData import StockChartData
from threading import Thread
import time
from datetime import datetime
from .database import StockCodeEntity, StockChartEntity
from .database.Core import SessionLocal
from multiprocessing import Pool, cpu_count

from .database.service.CodeService import get_code_name_list


class ThreadWrapper:
    def __init__(self, code_list):
        self.code_list = code_list

    async def run(self):
        start = time.time()
        print(start)
        while self.code_list:
            code = self.code_list.pop(0)
            maxDate = datetime.now().strftime('%Y%m%d')
            task = StockChartData(maxDate)
            await task(code)


datas = []
codeList = []


def getData(code):
    global datas
    maxDate = datetime.now().strftime('%Y%m%d')
    task = StockChartData(maxDate)
    datas += task.get(code)
    while task.obj.Continue:
        datas += task.get(code)
    # datas += data

def requestCode():
    global codeList,codes
    codes = [c[0].code for c in get_code_name_list()]
    start = time.time()
    print(f"requestCode Start {len(codes)}")
    while len(codes) > 0:
        if time.time() - start > 1:
            codeList.append(codes.pop(0))


def requestData():
    global codeList
    print("requestData Start")
    while True:
        if len(codeList) > 0:
            code = codeList.pop(0)
            getData(code)


def saveData():
    print("saveData Start")
    with SessionLocal() as session:
        while True:
            print(f"\r{len(datas)}\r", end="")
            if len(datas) > 0:
                d = datas.pop(0)
                smpt = select(StockChartEntity).filter(and_(
                    StockChartEntity.code == d.code, StockChartEntity.date == d.date, StockChartEntity.time == d.time))
                c = session.execute(smpt).all()
                if c.__len__() == 0:
                    session.add(d)
                    session.commit()


threads = [Thread(target=requestCode),
           Thread(target=requestData),
           Thread(target=requestData)
           ]
for _ in range(5):
    threads.append(Thread(target=saveData))

for t in threads:
    t.start()
