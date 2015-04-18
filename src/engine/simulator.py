# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from .asset import AssetState

def simulate(return_sampler, portfolio_generator, initial_portfolio, initial_date, final_date):
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
    _ = portfolio.value()

    # Prices are arbitrary at this point.
    asset_states = { name: AssetState(price=10.00) for name in asset_universe_names }
    asset_states['CASH'] = AssetState(price=1.00)

    period = return_sampler.return_period

    portfolio.update_asset_states(asset_states)

    # Make the initial state part of the series
    portfolio_value_series = [ ( date, portfolio.value() ) ]

    while (date < final_date):
        # Advance to next date.
        date += period

        # Sample returns and update the state of the world.
        returns = return_sampler.sample_returns()
        returns['CASH'] = 0.00  # Hackish: provide a working approach when the portfolio
                                # generator doesn't care about CASH.
        for name, prev_state in asset_states.iteritems():
            asset_states[name].price = prev_state.price * (1.0+returns[name])

        portfolio.update_asset_states(asset_states)  # The portfolio value changes here.
        portfolio = portfolio_generator.next_portfolio(portfolio, asset_states, date)

        portfolio_value_series.append( ( date, portfolio.value() ) )


    return portfolio_value_series