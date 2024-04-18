from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import select

from .database.Core import SessionLocal
from .database.models.StockData import StockChartEntity
from fastapi import FastAPI

app = FastAPI()


class Items(BaseModel):
    code: Optional[str]
    date: Optional[str]
    time: Optional[str]
    startPrice: Optional[float]
    highPrice: Optional[float]
    lowPrice: Optional[float]
    closePrice: Optional[float]
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


@app.get(path="/", response_model=List[Items])
def index():
    with SessionLocal() as session:
        return session.query(StockChartEntity).filter(StockChartEntity.code == "A000020").order_by(
            StockChartEntity.date.desc(), StockChartEntity.time.desc()).offset(0).limit(100).all()
