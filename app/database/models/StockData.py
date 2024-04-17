from sqlalchemy import Column, ForeignKey, String, DOUBLE, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from ..Core import BaseEntity


class StockChartEntity(BaseEntity):
    __tablename__ = 'TB_STOCK_CHART'

    code = Column("CODE", String(20), ForeignKey('TB_STOCK_CODE.CODE'), comment="코드")
    codeItem = relationship("StockCodeEntity", backref="stockChart")
    date = Column("DATE", DOUBLE,default=0.0)
    time = Column("TIME", DOUBLE, default=0.0)
    startPrice = Column("START_PRICE", DOUBLE, default=0.0)
    highPrice = Column("HIGHP_RICE", DOUBLE, default=0.0)
    lowPrice = Column("LOW_PRICE", DOUBLE, default=0.0)
    closePrice = Column("CLOSE_PRICE", DOUBLE, default=0.0)
    comparedToThePreviousDay = Column("COMPARED_TO_THE_PREVIOUS_DAY", DOUBLE, default=0.0)
    volume = Column("volume", DOUBLE, default=0.0)
    tradingValue = Column("TRADING_VALUE", DOUBLE, default=0.0)
    cumulativeSoldQuantity = Column("CUMULATIVE_SOLD_QUANTITY", DOUBLE, default=0.0)
    cumulativeTransactionQuantity = Column("CUMULATIVE_TRANSACTION_QUANTITY", DOUBLE, default=0.0)
    numberOfListedStocks = Column("NUMBER_OF_LISTED_STOCKS", DOUBLE, default=0.0)
    marketCapitalization = Column("MARKET_CAPITALIZATION", DOUBLE, default=0.0)
    foreignOrderLimitQuantity = Column("FOREIGN_ORDER_LIMIT_QUANTITY", DOUBLE, default=0.0)
    quantityAvailableForForeignersToOrder = Column("QUANTITY_AVAILABLE_FOR_FOREIGNERS_TO_ORDER", DOUBLE, default=0.0)
    foreignersCurrentHoldings = Column("FOREIGNERS_CURRENT_HOLDINGS", DOUBLE, default=0.0)
    foreignCurrentHoldingRatio = Column("FOREIGN_CURRENT_HOLDING_RATIO", DOUBLE, default=0.0)
    dateOfRevisedStockPrice = Column("DATE_OF_REVISED_STOCK_PRICE", DOUBLE, default=0.0)
    modifiedStockPriceRatio = Column("MODIFIEDSTOCK_PRICE_RATIO", DOUBLE, default=0.0)
    institutionalNetPurchaseVolume = Column("INSTITUTIONAL_NET_PURCHASE_VOLUME", DOUBLE, default=0.0)
    cumulativeInstitutionalNetPurchaseVolume = Column("CUMULATIVE_INSTITUTIONAL_NET_PURCHASE_VOLUME", DOUBLE,
                                                      default=0.0)
    arrangementForArrivalAndDeparture = Column("ARRANGEMENT_FOR_ARRIVAL_AND_DEPARTURE", DOUBLE, default=0.0)
    fluctuatingRate = Column("FLUCTUATING_RATE", DOUBLE, default=0.0)
    deposit = Column("DEPOSIT", DOUBLE, default=0.0)
    stockTurnover = Column("STOCK_TURNOVER", DOUBLE, default=0.0)
    transactionCompletionRate = Column("TRANSACTION_COMPLETION_RATE", DOUBLE, default=0.0)
    contrastMark = Column("CONTRAST_MARK", DOUBLE, default=0.0)
    executionPriceComparisonTransactionSaleQuantity = Column("EXECUTION_PRICE_COMPARISON_TRANSACTION_SALE_QUANTITY",
                                                             DOUBLE,
                                                             default=0.0)
    executionPriceComparisonTransactionQuantity = Column("EXECUTION_PRICE_COMPARISON_TRANSACTION_QUANTITY", DOUBLE,
                                                         default=0.0)

    __table_args__ = (
        PrimaryKeyConstraint("CODE", "DATE", "TIME"),
        {},
    )
