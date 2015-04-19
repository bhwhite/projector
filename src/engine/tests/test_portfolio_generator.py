# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from ..asset import Asset, AssetState
from ..holding import Holding
from ..portfolio import Portfolio
from .. import portfolio_generator

import unittest

class StubAssetCollection(object):
    def __getitem__(self, item):
        return Asset(item, item, item)


class PortfolioGeneratorTest(unittest.TestCase):
    def test_fixed_composition_generator(self):
        p = Portfolio(holdings=[ Holding(Asset('SPX', '', ''), 5),
                                 Holding(Asset('TYX', '', ''), 10) ],
                      asset_states=[ AssetState(price=19.0),
                                     AssetState(price=39.0) ])

        target_composition = {'TYX': 0.50, 'SPX': 0.50}
        pgen = portfolio_generator.FixedCompositionPortfolioGenerator(composition=target_composition)
        self.assertEqual(2, len(pgen.asset_names_of_interest()))
        self.assertIn('TYX',   pgen.asset_names_of_interest())
        self.assertIn('SPX', pgen.asset_names_of_interest())

        # Use same asset states as in p's construction
        current_asset_states = { 'SPX': AssetState(price=20.0), 'TYX': AssetState(price=40.0) }

        p.update_asset_states(current_asset_states)   # Pre-condition for next_portfolio
        next_p = pgen.next_portfolio(p, current_asset_states, date=None)

        # Value of portfolio should not be changed by re-composing it.
        self.assertAlmostEqual(p.value(), next_p.value())

        self.assertEqual(len(target_composition), len(next_p.holdings))

        for name, target_frac in target_composition.items():
            holding = next(h for h in next_p.holdings if h.asset.name == name)
            # TODO (nmusolino): assert uniqueness?

            price = current_asset_states[name].price

            observed_frac = holding.quantity * price / next_p.value()

            self.assertAlmostEqual(target_frac, observed_frac)
