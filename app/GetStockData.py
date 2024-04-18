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
            maxDate = datetime.now().strftime('%Y%m%d')

            task = StockChartData(maxDate)
            await task(code)


codeList = [c.code for c in get_code_name_list()]


def getData(codeList):
    gk = 0
    datas = []
    for code in codeList:
        max_date = None
        # max_date = get_min_date(code)
        if max_date is None:
            max_date = datetime.now().strftime('%Y%m%d')
        task = StockChartData(max_date)
        data = task.get(code)
        datas+=data
        gk += len(data)
        print("\r", code, " ===>", len(data)," ===>", gk, end="")
        # save_data_list(data)
        while task.obj.Continue:
            data = task.get(code)
            gk += len(data)
            print("\r", code, " ===>len", len(data)," ===>", gk, end="")
            # save_data_list(data)
            datas += data
        save_data(datas)


def save_data_list(data=[]):
    osc = len(data)
    ksc = 0
    for i in range(10):
        sp = len(data) // 10
        if i == 9:
            arg = data[i * sp:]
        else:
            arg = data[i * sp:(i + 1) * sp]
        ksc += len(arg)
        t = Thread(target=save_data, args=(arg,))
        t.start()


def save_data(data):
    with SessionLocal() as session:
        # i = 0
        # for d in datas:
        # for d in data:
        #     smpt = select(StockChartEntity).filter(and_(
        #         StockChartEntity.code == d.code, StockChartEntity.date == d.date, StockChartEntity.time == d.time))
        #     c = session.execute(smpt).all()
        #     if c.__len__() == 0:
        #         session.add(d)
        #         session.commit()
        #         i += 1
    # if i > 0:
        insert_stmt = insert(StockChartEntity).values(data)
        update_dict = {x.name: x for x in insert_stmt.inserted}
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(**update_dict)
        session.execute(on_duplicate_key_stmt)
        session.commit()
        # print(f"{d.code} : {i} =>inserted")


if __name__ == "__main__":
    procs = []

    p_list = []
    size = 12
    ck = 0
    for i in range(size):
        sp = (len(codeList) // size)
        if i == size - 1:
            sub_list = codeList[i * sp:]
        else:
            sub_list = codeList[i * sp:(i + 1) * sp]
        ck += len(sub_list)

        p = Process(target=getData, args=(sub_list,))
        p_list.append(p)

    print(len(codeList), "-=>", ck)
    for p in p_list:
        p.start()
