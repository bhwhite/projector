# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

class Asset(object):
    """
    An Asset represents the static nature of an investable security.  It does
    not describe its dynamic state at any point in time.
    """
    def __init__(self, name):
        self.name = name


class AssetState(object):
    """
    An AssetState represents the dynamic state of an Asset: its price,
    and in the future, its P/E ratio, earnings per share, and other
    properties.
    """
    def __init__(self, price=None):
        self.price = price

