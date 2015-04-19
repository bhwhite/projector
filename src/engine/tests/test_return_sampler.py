# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from .. import return_sampler

import datetime
import numbers
import unittest

class StubPortfolioGenerator(object):
    def __init__(self, asset_names):
        self.asset_names = set(asset_names)

    def asset_names_of_interest(self):
        return self.asset_names

class ReturnSamplerTest(unittest.TestCase):
    def test_fixed_return_sampler(self):
        # pgen = StubPortfolioGenerator({'TYX', 'SPX'})
        #
        # sampler = return_sampler.ConstantReturnSampler(portfolio_generator=pgen,
        #                                                start_date=datetime.date(year=2000, month=1, day=1),
        #                                                end_date=datetime.date(year=2014, month=12, day=31),
        #                                                return_period=datetime.timedelta(days=7))
        # sampled_returns = sampler.sample_returns()
        #
        # for name in pgen.asset_names_of_interest():
        #     self.assertIn(name, sampled_returns)
        #     self.assertIsInstance(sampled_returns[name], numbers.Real)
        #
        pass

    def test_fair_return_sampler(self):

        asset_names = {'TYX', 'SPX'}
        pgen = StubPortfolioGenerator(asset_names)

        sampler = return_sampler.FairHistoricalReturnSampler(portfolio_generator=pgen,
                                                             start_date=datetime.date(year=2000, month=1, day=1),
                                                             end_date=datetime.date(year=2014, month=12, day=31),
                                                             return_period=datetime.timedelta(days=7))

        for _ in xrange(10):
            r = sampler.sample_returns()
            for name in asset_names:
                self.assertIn(name, r)
                self.assertLess(-0.5, r[name])
                self.assertLess(r[name], 0.5)

