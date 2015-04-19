# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from ..output_formatters import highcharts_series

import datetime
import json
import unittest

class OutputFormattersTest(unittest.TestCase):
    def test_formatter(self):
        dates = [ datetime.date(2015, t, 15) for t in xrange(1, 12) ]
        all_portfolio_series = []
        for s_index in xrange(10):
           portfolio_series = list(zip(dates, xrange(100), xrange(s_index, s_index + len(dates))))
           all_portfolio_series.append(portfolio_series)

        highcharts_spec = highcharts_series(all_portfolio_series)

        import pprint
        pprint.pprint(highcharts_spec)

        unused = json.dumps(highcharts_spec)