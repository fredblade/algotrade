import backtrader as bt
import yfinance as yf

# Download data
data = yf.download("AAPL", start="2020-01-01", end="2021-01-01")
print(data.head())
data = data.dropna()

# SMA = Simple Moving Average
class SmaCross(bt.SignalStrategy):
    def __init__(self):
        # Create SMA for periods of 10 and 30
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        self.signal = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, self.signal)

    def __repr__(self):
        return f"SmaCross(sma1_period=10, sma2_period=30, signal={self.signal})"

cerebro = bt.Cerebro()
cerebro.addstrategy(SmaCross)
data = bt.feeds.PandasData(dataname=data)
cerebro.adddata(data)
result = cerebro.run()
# cerebro.plot()
# Print the expanded result
for strat in result:
    print(strat)