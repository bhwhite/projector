# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

class Holding(object):
    """
    A Holding is a component in a portfolio.  Right now, it represents a
    quantity (in units like shares, ounces, etc, that correspond to the price)
    and an Asset.

    In the future, this could hold information relating to history, like
    purchase date, cost basis, etc.
    """
    def __init__(self, asset, quantity):
        self.asset = asset
        self.quantity = quantity

