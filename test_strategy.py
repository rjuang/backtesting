import backtester
import data
import strategy

import datetime

data_reader = data.CachedDataReader()
tester = backtester.Backtester(data_reader)
dm = strategy.DualMomentum(data_reader, contribution=100)

tester.test(dm, starting_balance=1000)
