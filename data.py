import numpy as np
import pandas.io.data as web
import datetime

class CachedDataReader(object):
    def __init__(self):
        self._cache = {}

    def fetch(self, symbol, backend, start_date, end_date):
        key = (backend, symbol)
        if key not in self._cache:
            data = web.DataReader(symbol, backend,
                    datetime.date(1970, 1, 1), datetime.date.today())
            self._cache[key] = data

        data = self._cache[key]
        return data.ix[np.logical_and(start_date.isoformat() <= data.index,
            data.index <= end_date.isoformat())]

    def saveCache(self, filename):
        with open(filename, mode='wb') as f:
            pickle.dump(self._cache, f)

    def loadCache(self, filename):
        with open(filename, mode='rb') as f:
            data = pickle.load(f)
            self._cache = data
