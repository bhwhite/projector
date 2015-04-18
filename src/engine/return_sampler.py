# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

class ReturnSampler(object):
    """
    A ReturnSampler is designed to efficiently sample return values at random
    from a historical dataset.
    """
    def __init__(self, asset_names_of_interest, start_date, end_date, return_period):
        """
        :param assets_of_interest:  an iterable collection of asset names (str)
        :param start_date: the desired start date for the historical data sampling
        :param end_date: the desired end date for the historical data sampling
        :param return_period: the period for which returns are desired (e.g. one week
            one month, etc)
        :return:
        """
        self.asset_names_of_interest = asset_names_of_interest
        self.return_period = return_period


    def asset_names_of_interest(self):
        """
        Return a set containing the names of all assets for which this PortfolioGenerator
        will provide sample returns for.
        """
        return self.asset_names_of_interest


    def sample_returns(self):
        return NotImplementedError


class ConstantReturnSampler(ReturnSampler):
    """
    A stub class that returns a reasonable, constant return for all assets of interest.
    """
    def __init__(self, asset_names_of_interest, start_date, end_date, return_period):
        ReturnSampler.__init__(self, asset_names_of_interest, start_date, end_date, return_period)
        self.constant_return = 0.06 / (365 / self.return_period.days)


    def sample_returns(self):
        return { name: self.constant_return for name in self.asset_names_of_interest }
