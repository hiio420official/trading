import os
import time
from threading import Thread

import win32com.client
from dotenv import load_dotenv
from pywinauto import application

from app.win import Win32Function

load_dotenv()

class Cybos:
    g_objCpStatus = None

    def __init__(self):
        self.g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
        self.ID = os.getenv("ID")
        self.PW = os.getenv("PW")
        self.CERTPW = os.getenv("CERTPW")

    def kill_client(self):
        print("########## 기존 CYBOS 프로세스 강제 종료")
        os.system('taskkill /IM ncStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%ncStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    def connect(self):
        if not self.connected():
            self.disconnect()
            self.kill_client()

            print("########## CYBOS 프로세스 자동 접속")
            app = application.Application()
            # cybos plus를 정보 조회로만 사용했기 때문에 인증서 비밀번호는 입력하지 않았다.
            app.start(
                f'C:\\DAISHIN\\STARTER\\ncStarter.exe /prj:cp /id:{self.ID} /pwd:{self.PW} /pwdcert:{self.CERTPW} /autostart'
            )
            noti_title = Win32Function.check_window("공지사항", 60)
            if noti_title != 0:
                print("공지사항")
                Win32Function.close_win("공지사항")
            self.connect()
        else:
            i = 0
            while True:
                if self.connected():
                    # for i in range(60):
                    print(f"\r 접속중 ...{i}", end="")

                else:
                    self.connect()

    def connected(self):
        b_connected = self.g_objCpStatus.IsConnect
        if b_connected == 0:
            return False
        return True

    def disconnect(self):
        if self.connected():
            self.g_objCpStatus.PlusDisconnect()

    def waitForRequest(self):
        remainCount = self.g_objCpStatus.GetLimitRemainCount(1)
        if remainCount <= 0:
            time.sleep(self.g_objCpStatus.LimitRequestRemainTime / 1000)

    def checkSecuriry(self):
        noti_title = Win32Function.check_window("AhnLab Online Security", 60)
        if noti_title != 0:
            print("공지사항")
            Win32Function.close_win("AhnLab Online Security")
        else:
            print("없습니다.")

    def run(self):
        t = Thread(target=self.connect)
        t.start()
        t.join()
