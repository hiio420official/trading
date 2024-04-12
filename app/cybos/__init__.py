# import win32com.client
# from app.win import Win32Function
#
# from threading import Thread
#
#
# import win32com.client
# from pywinauto import application
# import os
# import time
#
#
# class StockCodeName(Cybos):
#
#     def __init__(self):
#         super().__init__()
#
#
#     def get(self):
#         if not self.connected():
#             print("self.stockConn.conn",self.connected())
#             return
#         else:
#             print("접속중")
#         # 종목코드 리스트 구하기
#         objCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
#         codeList = objCpCodeMgr.GetStockListByMarket(1) #거래소
#         codeList2 = objCpCodeMgr.GetStockListByMarket(2) #코스닥
#         data = []
#         print("거래소 종목코드", len(codeList))
#         for i, code in enumerate(codeList):
#             secondCode = objCpCodeMgr.GetStockSectionKind(code)
#             name = objCpCodeMgr.CodeToName(code)
#
#             stdPrice = objCpCodeMgr.GetStockStdPrice(code)
#             data += [{"code":code,"name":name}]
#
#         return data
#
#