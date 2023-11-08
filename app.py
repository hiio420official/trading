from config import stock
from libs.cybos import Cybos

if __name__ == "__main__":
    print(stock.ID)
    c = Cybos()
    c.connect(stock.ID,stock.PW,stock.CERTPW)