import backtester
import data
import strategy

import datetime

data_reader = data.CachedDataReader()
tester = backtester.Backtester(data_reader)

dca = strategy.DollarCostAverage(100)
tester.test(dca, starting_balance=1000)
