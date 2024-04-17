import asyncio

from sqlalchemy import select, func, and_

from .cybos.StockChartData import StockChartData
from threading import Thread
import time
from datetime import datetime
from .database import StockCodeEntity, StockChartEntity
from .database.Core import SessionLocal
from multiprocessing import Pool, cpu_count


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


def getData():
    global datas
    with SessionLocal() as session:
        li = session.execute(select(StockCodeEntity)).all()

        li = [la[0].code for la in li]
        # li = ["A000020"]
        maxDate = datetime.now().strftime('%Y%m%d')
        size = 5
        rn = len(li) // size

        print(len(li))
        for code in li:
            task = StockChartData(maxDate)
            datas +=task.get(code)
            while task.obj.Continue:
                datas +=task.get(code)


def saveData():
    with SessionLocal() as session:
        while True:
            print(f"\r{len(datas)}",end="")
            if len(datas)>0:

                d = datas.pop(0)

                smpt = select(StockChartEntity).filter(and_(
                    StockChartEntity.code == d.code, StockChartEntity.date == d.date, StockChartEntity.time == d.time))
                c = session.execute(smpt).all()

                if c.__len__() == 0:
                    print(d.code, d.date, d.time, len(c))
                    session.add(d)
                    session.commit()


threads = [Thread(target=getData)]
for _ in range(100):
    threads.append(Thread(target=saveData))

for t in threads:
    t.start()

# for i in range(size):
#     if i == size - 1:
#         comma = li[i * rn:]
#     else:
#         comma = li[i * rn:(i + 1) * rn]
#     print(len(comma))
#     t = ThreadWrapper(comma)
#     asyncio.run(t.run())
# threads.append(asyncio.create_task(t.run()))
# await asyncio.wait()
# await asyncio.gather(*threads)
# asyncio.run(main())
#     print(len(comma))
#     threads.append(t)
# for t in threads:
#     t.start()
#     t.join()
# for code in li:
#
#
#     print(maxDate)
#     task = StockChartData(code, maxDate)
#     task()
