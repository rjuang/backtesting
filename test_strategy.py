import backtester
import strategy

import datetime

tester = backtester.Backtester()
dca = strategy.DollarCostAverage(1000)
dm = strategy.DualMomentum()

#tester.test(dca, starting_balance=1000)
tester.test(dm, starting_balance=1000)
#, start_date=datetime.date(2009, 1,1))
