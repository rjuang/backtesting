from pandas.io.data import DataReader
import datetime


class Portfolio(object):
    def __init__(self):
        self._current_holdings = []
        self._current_cash = 0
        self._current_date = None
        self._total_cash_input = 0

    def _nextClosingPrice(self, symbol):
        date = self._current_date
        for _ in range(5):
            try:
                stock = DataReader(symbol, 'yahoo', date)
                if stock.empty:
                    date = date - datetime.timedelta(days=1)
                    continue
                break
            except IndexError:
                pass

        return stock['Adj Close'][0]

    def setDate(self, date):
        self._current_date = date

    def resetBalance(self, cash):
        self._current_cash = cash
        self._total_cash_input = cash
        self._current_holdings = []

    def networth(self):
        total = self._current_cash
        for num_shares, symbol in self._current_holdings:
            total += num_shares * self._nextClosingPrice(symbol)
        return total

    def rebalance(self, newplan):
        cash = self.networth()
        newholdings = []
        for fraction, symbol in newplan:
            price = self._nextClosingPrice(symbol)
            num_shares = (cash * fraction) / price
            newholdings.append((num_shares, symbol))
        self._current_holdings = newholdings
        self._current_cash = 0.0

    def addCash(self, amount):
        self._current_cash += amount
        self._total_cash_input += amount

    def sellAll(self):
        self._current_cash = self.networth()
        self._current_holdings = []

    def currentHoldings(self):
        return list(self._current_holdings)

    def totalCashInput(self):
        return self._total_cash_input
