# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from .. import return_sampler

import datetime
import unittest


class ReturnSamplerTest(unittest.TestCase):
    def test_fixed_return_sampler(self):

        sampler = return_sampler.ConstantReturnSampler(asset_names_of_interest={ 'BND', 'SP500' },
                                                       start_date=datetime.date(year=2000, month=1, day=1),
                                                       end_date=datetime.date(year=2014, month=12, day=31),
                                                       return_period=datetime.timedelta(days=7))
        sampled_returns = sampler.sample_returns()

        self.assertIn('BND', sampled_returns)
        self.assertIn('SP500', sampled_returns)
