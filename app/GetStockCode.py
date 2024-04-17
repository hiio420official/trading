from .cybos.StockCodeName import StockCodeName
# from .database.Core import engine,BaseEntity

com = StockCodeName()
data = com.get()
print(data)
com.save(data)