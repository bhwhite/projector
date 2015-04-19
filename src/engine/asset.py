# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

class Asset(object):
    """
    An Asset represents the static nature of an investable security.  It does
    not describe its dynamic state at any point in time.
    """
    def __init__(self, name, display_name, ticker):
        self.name = name
        self.display_name = display_name
        self.ticker = ticker


class AssetState(object):
    """
    An AssetState represents the dynamic state of an Asset: its price,
    and in the future, its P/E ratio, earnings per share, and other
    properties.
    """
    def __init__(self, price=None):
        self.price = price

ASSETS = { asset.name: asset for asset in ( Asset('CASH', 'Cash', 'Cash'),
                                            Asset('SPX', 'S&P500 Index', '^GSPC'),
                                            Asset('TYX', 'US 30 Year Treasuries', '^TYX'), )
           }
