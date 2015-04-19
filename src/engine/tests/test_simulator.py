# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from ..asset import Asset, AssetState, ASSETS
from ..holding import Holding
from ..portfolio import Portfolio
from .. import return_sampler
from .. import portfolio_generator
from .. import simulator

import datetime
import pprint
import time  # for timing
import unittest

class Timer(object):
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

def noop(_):
    return 0


class SimulatorTest(unittest.TestCase):
    def test_simulator(self):
        pgen = portfolio_generator.FixedCompositionPortfolioGenerator({ 'TYX': 0.25, 'SPX': 0.75 })

        return_period = datetime.timedelta(days=7)
        sampler = return_sampler.FairHistoricalReturnSampler(portfolio_generator=pgen,
                                                             start_date=datetime.date(year=2000, month=1, day=1),
                                                             end_date=datetime.date(year=2014, month=12, day=31),
                                                             return_period=return_period)


        cash_asset_state = AssetState(price=1.00)
        initial_portfolio = Portfolio(holdings=[ Holding(ASSETS['CASH'], quantity=10000)],
                                      asset_states=[cash_asset_state])
        # Confirm this does not throw
        initial_portfolio_value = initial_portfolio.value()

        start_date = datetime.date(year=2015, month=4, day=18)
        end_date = start_date + datetime.timedelta(days=20 * 365.25)

        annual_contribution_amount = 365.25

        with Timer() as t:
            port_value_series = simulator.simulate(return_sampler=sampler,
                                                   initial_portfolio=initial_portfolio,
                                                   portfolio_generator=pgen,
                                                   initial_date=start_date,
                                                   final_date=end_date,
                                                   annual_contribution_amount=annual_contribution_amount)

        print("simulator output:\n{}\n...\n{}".format(pprint.pformat(port_value_series[1:4]),
                                                      pprint.pformat(port_value_series[-4:])))
        print("Single simulation overhead: {}".format(t.interval))

        def approx_equal(a, b, rel_tol):
            return abs(a - b) < rel_tol * 0.5 * (a+b)

        self.assertTrue(approx_equal(initial_portfolio_value + annual_contribution_amount*20,
                                     port_value_series[-1][1],
                                     rel_tol=0.01))


    def test_pool_overhead(self):
        import multiprocessing

        with Timer() as t:
            pool = multiprocessing.Pool(8)
            results = pool.map(noop, xrange(100))

        print("Multiprocessing overhead: {}".format(t.interval))
