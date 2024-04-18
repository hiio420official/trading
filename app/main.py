from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import select
from starlette.middleware.cors import CORSMiddleware

from .database.Core import SessionLocal
from .database.models.StockData import StockChartEntity
from fastapi import FastAPI

app = FastAPI()


class Items(BaseModel):
    code: Optional[str]
    date: Optional[int]
    time: Optional[int]
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    comparedToThePreviousDay: Optional[float]
    volume: Optional[float]
    tradingValue: Optional[float]
    cumulativeSoldQuantity: Optional[float]
    cumulativeTransactionQuantity: Optional[float]
    numberOfListedStocks: Optional[float]
    marketCapitalization: Optional[float]
    foreignOrderLimitQuantity: Optional[float]
    quantityAvailableForForeignersToOrder: Optional[float]
    foreignersCurrentHoldings: Optional[float]
    foreignCurrentHoldingRatio: Optional[float]
    dateOfRevisedStockPrice: Optional[float]
    modifiedStockPriceRatio: Optional[float]
    institutionalNetPurchaseVolume: Optional[float]
    cumulativeInstitutionalNetPurchaseVolume: Optional[float]
    arrangementForArrivalAndDeparture: Optional[float]
    fluctuatingRate: Optional[float]
    deposit: Optional[float]
    stockTurnover: Optional[float]
    transactionCompletionRate: Optional[float]
    contrastMark: Optional[float]
    executionPriceComparisonTransactionSaleQuantity: Optional[float]
    executionPriceComparisonTransactionQuantity: Optional[float]

    class Config:
        from_attribute = True
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
@app.get(path="/", response_model=List[Items])
def index(code:Optional[str],offset:Optional[int] = 0,limit:Optional[int] =0):
    with SessionLocal() as session:
        return session.query(StockChartEntity).filter(StockChartEntity.code == code).order_by(
            StockChartEntity.date.desc(), StockChartEntity.time.desc()).offset(offset).limit(limit).all()
