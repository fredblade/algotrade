import backtrader as bt
import yfinance as yf

#Download data
data = yf.download("AAPL", start="2020-01-01", end="2021-01-01")
print(data.head())
data = data.dropna()


# SMA = Simple Moving Average
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        #cree SMA pour period de 10 et 30 (2graph separe)
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma1, sma2))

    
cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
data = bt.feeds.PandasData(dataname=data)
cerebro.adddata(data)
cerebro.run()
cerebro.plot()
