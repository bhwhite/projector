# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

from . import summarize

import json

# Our client-side code expects dates as "YYYY-MM-DD" strings.

def _portfolio_value_series(portfolio_series):
    """
    Return a timeseries (list of (datestring, value) tuples) of portfolio values
    from 'portfolio_series'.
    """
    return [ (str(elem[0]), elem[2]) for elem in portfolio_series ]

def _contribution_series(portfolio_series):
    """
    Return a timeseries (list of (datestring, contribution) tuples) of portfolio values
    from 'portfolio_series'.
    """
    return [ (str(elem[0]), elem[1]) for elem in portfolio_series ]


def _highcharts_minor_series(portfolio_series):
     return { 'name': '',
              'type': 'line',
              'lineWidth': 1,
              'showInLegend': False,
              'color': '#D0D6D6',
              'marker': { 'enabled': False },
              'data': _portfolio_value_series(portfolio_series)
            }

def _highcharts_median_series(portfolio_series):
    ## HACK!  We need to extract with the _contribution_series converter, because
    ## it gets elements 0 and 1 from each tuple.
    return { 'name': 'Median portfolio value',
              'type': 'line',
              'color': '#09388F', # Dark blue
              'lineWidth': 5,
              'marker': { 'enabled': False },
              'data': _contribution_series(portfolio_series)
            }


def _highcharts_envelope_series(portfolio_series, name):
    return { 'name': name,
              'type': 'line',
              'color': '#597EC2', # Middle blue
              'lineWidth': 3,
              'marker': { 'enabled': False },
              'data': _contribution_series(portfolio_series)
            }


def _highcharts_contribution_series(portfolio_series):
    return { 'name': 'Cumulative contributions',
              'type': 'area',
              'color': 'red',
              'data': _contribution_series(portfolio_series)
            }

def _highcharts_add_goal(goal_series):
    return { 'name': 'Goal',
             'type': 'line',
             'color': '#22610B',
             'marker': { 'enabled': False },
             'data': _contribution_series(goal_series)
           }



def highcharts_series(all_portfolio_series, goal_value=None):
    """
    This function conflates output formatting and output summarizing.
    :param all_portfolio_series:
    :return:
    """
    # Contributions will be the same in all output series.
    # charting_spec = [ _highcharts_contribution_series(all_portfolio_series[0]) ]

    charting_spec = []
    charting_spec.append(_highcharts_contribution_series(all_portfolio_series[0]))

    # Add the individual trajectories
    for series in all_portfolio_series:
        charting_spec.append(_highcharts_minor_series(series))

    # Add summary.
    summary = summarize.summarize_series(all_portfolio_series, sampling_freq=2)

    charting_spec.append(_highcharts_median_series(summary['P50']))
    for percentile in (10, 90):
        charting_spec.append(_highcharts_envelope_series(summary['P{}'.format(percentile)],
                                                         name='{}th percentile'.format(percentile)))

    if goal_value is not None and goal_value > 0.1:
        start_date = all_portfolio_series[0][0][0]
        end_date = all_portfolio_series[0][-1][0]
        goal_series = [ (start_date, goal_value),
                        (end_date,   goal_value) ]
        charting_spec.append(_highcharts_add_goal(goal_series))

    _ = json.dumps(charting_spec)

    return charting_spec

