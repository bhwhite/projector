# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from .. import summarize

import datetime
import itertools
import unittest

class Timer(object):
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

class Summarizer(unittest.TestCase):
    def test_summarizer(self):
        dates = [ datetime.date(2015, t, 15) for t in xrange(1, 12) ]
        cumulative_contributions = 1
        for sampling_freq in (1, 2):
            all_portfolio_series = []

            for s_index in xrange(10):
                portfolio_series = zip(dates, itertools.repeat(cumulative_contributions), xrange(s_index, s_index + len(dates)))
                all_portfolio_series.append(portfolio_series)

            summary = summarize.summarize_series(all_portfolio_series, sampling_freq=sampling_freq)

            self.assertTrue(summary)

            self.assertIn('P10', summary)
            self.assertIn('P50', summary)
            self.assertIn('P90', summary)





