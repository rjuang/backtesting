import datetime
import numpy as np
import operator

class Strategy(object):
    def evaluate(self, date):
        """ Evaluate strategy.

        Params:
          date:  date to evaluate strategy

        Returns:
          a tuple (action, cash_to_add) where tuple contains a list of tuples
          specifying (fraction of portfolio, symbol) portfolio.
        """
        return [], 0


class DollarCostAverage(Strategy):
    """ Dollar cost average is just to keep throwing a consistent amount of
    money into total market funds every regular interval. """
    def __init__(self, amount, plan=None):
        self._amount = amount
        if plan is None:
            plan = [(1.0, 'SPY')]
        self._plan = plan

    def evaluate(self, date):
        return self._plan, self._amount


class DualMomentum(Strategy):
    def __init__(self, data_reader, contribution=100):
        self.today = datetime.date.today()
        self.amount = contribution
        self.data_reader = data_reader

    def _getHistoricalPrice(self, symbol, start_date, end_date):
        # stock = DataReader(symbol, 'yahoo', start_date, end_date)
        stock = self.data_reader.fetch(symbol, 'yahoo', start_date, end_date)
        return list(reversed(stock['Adj Close']))

    def _volatility(self, prices):
        return np.std(prices)

    def _semivolatility(self, prices):
        prices = np.array(prices)
        return np.std(prices[prices < np.mean(prices)]) / np.mean(prices)

    def _getPerformance(self, prices, num_days):
        prices = prices[:num_days]
        return (prices[0] - prices[-1]) / prices[-1]

    def _getRanking(self, symbol):
        start_date = self.today - datetime.timedelta(days=365)
        prices = self._getHistoricalPrice(symbol, start_date, self.today)

        rank = (0.5 * self._getPerformance(prices, 91) +
                0.3 * self._getPerformance(prices, 182) -
                0.2 * self._semivolatility(prices[:63]))
        return rank

    def getMomentumDecision(self):
        options = {
#                   'VNQ': 'Real Estate',
#                   'VTI': 'US Equities',
#                   'TLT': 'Long-Term treasuries',
#                   'SHY': 'Cash',
#                   'PCY': 'Emerging Market Debt',
#                   'TIP': 'Treasury Inflated Protected Securities',
#                   'VWO': 'Emerging Markets',
#                   'RWX': 'International Real Estate',
#                   'VEA': 'Developed Markets',
#                   'GLD': 'Gold',
#                   'DBC': 'Commodities'

#                   'SPY': 'US Equities',
#                   'TIP': 'Treasury Inflated Protected Securities',
#                   'TLT': 'Long-term treasuries',
                   'DBC': 'Commodities',
                   'GLD': 'Gold',
                    'SPY': 'S&P 500',
#                    'ACWX': 'World index',
#                    'BIL': 'US Treasury bills',
#                    'BND': 'Aggregate bonds',
}
        baseline = 'SPY'

        performance = {s: self._getRanking(s) for s in options.keys()}
        sorted_perf = sorted(performance.items(), key=operator.itemgetter(1),
                reverse=True)

#        if sorted_perf[0][0] == baseline:
#            return [(1.0, baseline)]

        return [(0.5, sorted_perf[0][0]),
                (0.5, sorted_perf[1][0])]

    def evaluate(self, date):
        self.today = date
        plan = self.getMomentumDecision()
        return plan, self.amount


