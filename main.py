from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import pandas as pd
from SMAStrat import SMAStrategy

# PARAMS
initialCash = 1000
startDate='2024-01-01'
endDate='2024-09-01'
csvPath='data/AAPL.csv'

# Create a cerebro entity and add a strategy
cerebro = bt.Cerebro()
cerebro.addstrategy(SMAStrategy)

# Load the CSV using pandas
df = pd.read_csv(csvPath)

# Remove the dollar signs from price columns and convert to float
df['Close/Last'] = df['Close/Last'].replace({'\$': ''}, regex=True).astype(float)
df['Open'] = df['Open'].replace({'\$': ''}, regex=True).astype(float)
df['High'] = df['High'].replace({'\$': ''}, regex=True).astype(float)
df['Low'] = df['Low'].replace({'\$': ''}, regex=True).astype(float)

# Convert 'Date' column to datetime with MM/DD/YYYY format
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Rename columns to match Backtrader naming conventions
df.rename(columns={'Close/Last': 'close', 'Volume': 'volume', 'Open': 'open', 'High': 'high', 'Low': 'low'},
          inplace=True)

#Reverse the order of the dataframe
df = df.iloc[::-1]
# Define your data feed
data = bt.feeds.PandasData(dataname=df, fromdate=pd.Timestamp(startDate), todate=pd.Timestamp(endDate))

# Add the Data Feed to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(initialCash)

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
cerebro.run()
cerebro.plot()
# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())