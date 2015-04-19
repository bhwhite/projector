# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from .portfolio_generator import PortfolioGenerator

import datetime
import random

HISTORICAL_RETURNS = None

class ReturnSampler(object):
    """
    A ReturnSampler is designed to efficiently sample return values at random
    from a historical dataset.
    """
    def __init__(self, portfolio_generator, start_date, end_date, return_period):
        """
        :param portfolio_generator: the portfolio_generator, which supplies the assets of interest
        :param start_date: the desired start date for the historical data sampling
        :param end_date: the desired end date for the historical data sampling
        :return:
        """
        self.portfolio_generator = portfolio_generator
        self.return_period = return_period

    def sample_returns(self):
        return NotImplementedError


class FairHistoricalReturnSampler(ReturnSampler):
    """ Returns a fairly-sampled historical return"""

    def __init__(self, portfolio_generator, start_date, end_date, return_period):
        ReturnSampler.__init__(self, portfolio_generator, start_date, end_date, return_period)

    def sample_returns(self):
        return random.choice(HISTORICAL_RETURNS)

class ConstantReturnSampler(ReturnSampler):
    """
    A stub class that returns a reasonable, constant return for all assets of interest.
    """
    def __init__(self, portfolio_generator, start_date, end_date, return_period):
        ReturnSampler.__init__(self, portfolio_generator, start_date, end_date, return_period)
        self.constant_return = return_period.days * (0.06 / 365.25)


    def sample_returns(self):
        return { name: self.constant_return for name in self.portfolio_generator.asset_names_of_interest() }


RETURN_SAMPLERS = { 'Constant 6% Annual' : lambda aa, bb, cc: ConstantReturnSampler(aa, bb, cc, datetime.timedelta(days=7)),
                    'Historical Returns' : lambda aa, bb, cc: FairHistoricalReturnSampler(aa, bb, cc, datetime.timedelta(days=7)),
                    }
