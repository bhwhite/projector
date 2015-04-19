# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from __future__ import division

from .asset import AssetState, ASSETS
from .holding import Holding

def simulate(return_sampler, portfolio_generator, initial_portfolio, initial_date, final_date, annual_contribution_amount=0.0):
    """
    :param return_sampler:
    :param portfolio_generator:
    :param initial_portfolio:
    :param start_date:
    :param end_date:
    :return: A PortfolioTrajectory, which is a timeseries of portfolio value (and other properties)
    """

    asset_universe_names = portfolio_generator.asset_names_of_interest()

    date = initial_date
    portfolio = initial_portfolio

    # Confirm this does not throw.
    cumulative_contributions = portfolio.value()

    CASH_ASSET = ASSETS['CASH']
    CASH_ASSET_STATE  = AssetState(price=1.00)

    # Prices are arbitrary at this point.
    asset_states = { name: AssetState(price=10.00) for name in asset_universe_names }
    asset_states['CASH'] = CASH_ASSET_STATE
    portfolio.update_asset_states(asset_states)

    period = return_sampler.return_period

    period_contribution_amount = annual_contribution_amount * (period.days / 365.25)


    # Make the initial state part of the series
    portfolio_value_series = [ ( date, cumulative_contributions, portfolio.value() ) ]

    while (date < final_date):
        # Advance to next date.
        date += period

        # Sample returns and update the state of the world.
        returns = return_sampler.sample_returns()
        returns['CASH'] = 0.00  # Hackish: provide a working approach when the portfolio
                                # generator doesn't care about CASH.
        for name, prev_state in asset_states.iteritems():
            # import logging
            # logging.warn('name: {}, asset_states: {}, returns: {}'.format(name, asset_states, returns))
            asset_states[name].price = prev_state.price * (1.0+returns[name])

        portfolio.update_asset_states(asset_states)  # The portfolio value changes here.

        # Contribution happens at the end of the period.
        cumulative_contributions += period_contribution_amount
        portfolio.add_holding(Holding(CASH_ASSET, period_contribution_amount), CASH_ASSET_STATE)

        portfolio = portfolio_generator.next_portfolio(portfolio, asset_states, date)

        portfolio_value_series.append( ( date, cumulative_contributions, portfolio.value() ) )


    return portfolio_value_series
