from config import stock
from libs.cybos import Cybos,StockCodeName
import subprocess
if __name__ == "__main__":
    c = Cybos(stock.ID,stock.PW,stock.CERTPW)
    c.run()
    