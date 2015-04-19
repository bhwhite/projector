# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from ..asset import Asset, AssetState, ASSETS
from ..holding import Holding
from ..portfolio import Portfolio

import unittest

class PortfolioTest(unittest.TestCase):
    def test_value(self):
        p = Portfolio(holdings=[ Holding(Asset('SP500', '', ''), 5),
                                 Holding(Asset('BND', '', ''), 10) ],
                      asset_states=[ AssetState(price=7.0),
                                     AssetState(price=9.0) ])

        self.assertEqual(5*7.0 + 10*9.0, p.value())

    def test_value_update(self):
        p = Portfolio(holdings=[ Holding(Asset('SP500', '', ''), 5),
                                 Holding(Asset('BND', '', ''), 10) ])


        asset_states = { 'SP500': AssetState(price=7.0),
                         'BND':   AssetState(price=9.0) }
        p.update_asset_states(asset_states)
        self.assertEqual(5*7.0 + 10*9.0, p.value())

    def test_add_holding(self):
        asset_states = { 'SP500': AssetState(price=7.0),
                         'BND':   AssetState(price=9.0) }

        p = Portfolio(holdings=[ Holding(Asset('SP500', '', ''), 5),
                                 Holding(Asset('BND', '', ''), 10) ],
                      asset_states=[ AssetState(price=7.0),
                                     AssetState(price=9.0) ])

        prev_value = p.value()

        new_holding = Holding(ASSETS['CASH'], quantity=1000)
        cash_asset_state = AssetState(price=1.00)

        p.add_holding(new_holding, cash_asset_state)

        self.assertAlmostEqual(prev_value + new_holding.quantity * cash_asset_state.price,
                               p.value())