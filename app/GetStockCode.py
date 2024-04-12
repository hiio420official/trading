from .cybos.StockCodeName import StockCodeName
from .database.Core import engine,BaseEntity

BaseEntity.metadata.create_all(bind=engine)


com = StockCodeName()
data = com.get()
print(data)
com.save(data)