import datetime
import portfolio

class Backtester(object):
    def __init__(self):
        self.historical_networth = []
        self.historical_action = []
        self.historical_holdings = []
        self.historical_cash_input = []

        self.current_portfolio = portfolio.Portfolio()

    def test(self, strategy, start_date=None, end_date=None,
            starting_balance=10000, rebalance_period=33):
        if start_date is None:
            start_date = datetime.date(2001, 1, 1)
        if end_date is None:
            end_date = datetime.date.today()

        self.current_portfolio.resetBalance(starting_balance)
        self.current_portfolio.setDate(start_date)

        current_date = start_date
        delta = datetime.timedelta(days=rebalance_period)
        last_date = None

        while current_date < end_date:
            self.current_portfolio.setDate(current_date)
            action, cash_addition = strategy.evaluate(current_date)
            if cash_addition > 0:
                self.current_portfolio.addCash(cash_addition)
            self.current_portfolio.rebalance(action)
            self.historical_networth.append(
                    (current_date, self.current_portfolio.networth()))
            self.historical_action.append((current_date, action))
            self.historical_holdings.append(
                    (current_date, self.current_portfolio.currentHoldings()))
            self.historical_cash_input.append(
                    self.current_portfolio.totalCashInput())
            total_years = float((current_date - start_date).days) / 365.0
            total_input = self.current_portfolio.totalCashInput()
            gain = self.historical_networth[-1][-1] - total_input
            gain_pct = gain / total_input * 100.0
            gain_per_year = gain_pct / total_years

            print ('%s: Total = %0.3f | Total Input = %0.3f | '
                    'Change: = %0.3f [%0.3f %%] | %0.3f %% per year '
                    '(over %0.3f years)') % (
                    current_date.isoformat(),
                    self.historical_networth[-1][-1],
                    total_input,
                    gain, gain_pct, gain_per_year, total_years)

            current_date += delta
