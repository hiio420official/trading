from config import stock
from libs.cybos import Cybos

if __name__ == "__main__":
    c = Cybos()
    c.connect(stock.ID,stock.PW,stock.CERTPW)