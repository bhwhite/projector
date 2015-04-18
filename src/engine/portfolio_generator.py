# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from .asset import ASSETS
from .holding import Holding
from .portfolio import Portfolio

import collections

class PortfolioGenerator(object):
    def __init__(self):
        pass

    def asset_names_of_interest(self):
        """
        Return the names of all assets this PortfolioGenerator cares about.
        """
        raise NotImplementedError

    def next_portfolio(self, old_portfolio, current_asset_states, date):
        """
        This function returns a updated Portfolio based on the old portfolio,
        and the current state of all assets.

        :param old_portfolio: the Portfolio which acts as a starting point.
            This portfolio MUST have up-to-date asset states.
        :param current_asset_states: a dict from name to AssetStates.
            The assets described here should be a superset of everything this
            PortfolioGenerator cares about.
        :param date: the date for which the current asset state applies
        :return: a new Portfolio object
        """
        raise NotImplementedError


class FixedCompositionPortfolioGenerator(PortfolioGenerator):
    def __init__(self, composition):
        """
        :param composition: A dict from asset name (str) to fraction.
        """

        PortfolioGenerator.__init__(self)  # Init base class

        assert abs(sum(composition.itervalues()) - 1.0) < 1E-4   # Apply float tolerance
        self.composition = collections.OrderedDict(composition)

    def asset_names_of_interest(self):
        return set(self.composition.keys())

    def asset_names_of_interest(self):
        return set(self.composition.keys())


    def next_portfolio(self, old_portfolio, current_asset_states, date):
        total_value = old_portfolio.value()

        # This is done in a single list comprehension as an optimization.  Equivalent code:
        #
        #   new_holdings = []
        #   for name, frac in self.composition:
        #       current_price = current_asset_states[name].price
        #       new_qty = total_value * frac / current_asset_states[name].price
        #       asset = assets[name]
        #       new_holdings.append(Holding(asset, new_qty)
        
        new_holdings = [ Holding(ASSETS[name], total_value * frac / current_asset_states[name].price) for name, frac in self.composition.iteritems() ]
        asset_states = [ current_asset_states[name] for name in self.composition ]
        assert len(new_holdings) == len(asset_states)
        return Portfolio(new_holdings, asset_states)

PORTFOLIO_GENERATORS = {
    'Fixed Composition: 80% Stocks / 20% Bonds' : lambda: FixedCompositionPortfolioGenerator( { 'SP500' : .80, 'UST30' : .20 } ),
    }
