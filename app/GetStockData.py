import time
from datetime import datetime

from app.database.service.StockService import update_stock_data_record, select_stock_data_record
from .cybos.StockChartData import StockChartData
from .database.service.CodeService import get_code_name_list
from multiprocessing import Pool


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
    record = select_stock_data_record(code)
    date_list = []
    max_date = datetime.now().strftime('%Y%m%d')
    if record is not None:
        min_date = str(record.maxDatetime)[:8]
        if max_date > min_date:
            date_list.append({"max_date": "", "min_date": min_date})
        else:
            date_list.append({"max_date": "", "min_date": max_date})

        date_list.append({"max_date": str(record.minDatetime)[:8], "min_date": "19770101"})
    else:
        date_list.append({"max_date": max_date, "min_date": "19770101"})

    try:
        for dl in date_list:
            print(dl)
            task = StockChartData(dl["max_date"], dl["min_date"])
            data = task(code)
            update_stock_data_record({"code": code, "total": len(data), "errorLog": ""})
    except Exception as e:
        print(code, str(e))
        update_stock_data_record({"code": code, "errorLog": str(e)})


if __name__ == "__main__":
    # with Pool(10) as p:
    #     p.map(getData, codeList)
    i = 0
    for code in codeList:
        getData(code)
        i += 1
        print(i,code)
    # getData(codeList[0])
    # print(codeList[1235])
