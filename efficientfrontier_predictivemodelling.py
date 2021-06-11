from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


plt.style.use('fivethirtyeight')
#getting stocks data
assets = ['FB', 'AMZN', 'AAPL', 'NFLX']
stockSD ='2015-01-01'
today = datetime.today().strftime('%Y-%m-%d')
df = pd.DataFrame()

#store close price
for stock in assets:
  df[stock] = web.DataReader(stock, data_source='yahoo',start = stockSD, end = today)['Adj Close']
title = 'Portfolio Close Price History'

my_stocks = df
#plot graph
for c in my_stocks.columns.values:
  plt.plot(my_stocks[c], label = c)
plt.title(title)
plt.xlabel('Date')
plt.ylabel('Closing Price in USD')
plt.legend(my_stocks.columns.values, loc ='upper left')
#plt.show()
#daily returns
returns = df.pct_change()
#annualized cov_matrix
cov_matrix = returns.cov()*252 #no of trading days of this yr
#calc portfolio var
weights = np.array(np.random.random(4))
weights /= np.sum(weights)

port_var = np.dot(weights.T, np.dot(cov_matrix, weights))
#calc portfolio volatality sd
port_volatility = np.sqrt(port_var)
#calc annual portfolio returns
preturns = np.sum(returns.mean()*weights)* 252

#calc returns and sample cov matrix
mu = expected_returns.mean_historical_return(df)
S = risk_models.exp_cov(df)
#max sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights() #cleans the raw weights and sets abs values for those below cuttoff
print(cleaned_weights)
ef.portfolio_performance(verbose = True)

latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value = 10000)
allocation, leftover = da.lp_portfolio()
print(allocation)
print('Funds remaining: ${:.2f}'.format(leftover))