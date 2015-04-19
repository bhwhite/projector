# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

class Portfolio(object):
    def __init__(self, holdings, asset_states=None):
        """
        :param holdings:  a sequence of Holdings
        :param asset_states:  a sequence of AssetStates corresponding to the
            sequence of holdings, i.e. a parallel list.
        """
        if asset_states is not None:
            assert len(holdings) == len(asset_states)
            self.asset_states = list(asset_states)
        else:
            self.asset_states = None

        self.holdings = list(holdings)

        self._cached_value = None


    def update_asset_states(self, asset_states_dict):
        """
        Update the Portfolio's view of the state of the world.

        :param asset_states_dict:  a dict from asset name (str) to AssetStates.
            Must contain an entry for every Holding in self.holdings.
        """
        self.asset_states = [ asset_states_dict[h.asset.name] for h in self.holdings ]
        self._cached_value = None


    def add_holding(self, holding, asset_state):
        """
        Add the given holding with the described state to the Portfolio.
        :param holding:  a holding.  It is okay if this duplicates an Asset already
            held in the Portfolio.
        :param asset_state:  the corresponding AssetState
        """
        self.holdings.append(holding)
        self.asset_states.append(asset_state)
        self._cached_value = None

    def value(self):
        """
        Return the value of this portfolio
        :param asset_states:  a dict from asset name to asset states
        :return: the total value of all holdings in this portfolio
        """
        assert self.asset_states is not None
        assert len(self.holdings) == len(self.asset_states)

        if self._cached_value is not None:
            return self._cached_value
        else:
            self._cached_value = sum(h.quantity * a.price for (h, a) in zip(self.holdings, self.asset_states))
            return self._cached_value
