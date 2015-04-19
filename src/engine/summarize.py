# This file is part of Projector.
# Copyright 2015 Nicholas Musolino and Benjamin White
# For licensing terms, please see the LICENSE file distributed with this file.

def summarize_series(all_portfolio_series, sampling_freq=1):
    """
    Return a dict containing separate date series for 'P10', 'P50', 'P90'.
    Example return value:
      {
         'P10': [ [ "2015-05-01", 1000 ],
                  [ "2015-06-01", 1010 ],
                  ...
                  [ "2035-12-01", 9030 ]
                ],
         'P50': [ [ "2015-05-01", 1000 ],
                  [ "2015-06-01", 1025 ],
                  ...
                  [ "2035-12-01", 16742 ]
                ],
         etc
      }
    """
    if not all_portfolio_series:
        return None

    number_of_series = len(all_portfolio_series)
    key_series = all_portfolio_series[0]
    series_length = len(key_series)

    low_series_index = int(0.10 * number_of_series)
    med_series_index = int(0.50 * number_of_series)
    hi_series_index = int(0.90 * number_of_series)

    summary_series = []
    for i in xrange(0, series_length, sampling_freq):
        # i indexes every series, and picks out a consistent date in all series
        date = key_series[i][0]

        def portfolio_value(datapoint):
            return datapoint[2]

        observed_port_values = sorted((series[i] for series in all_portfolio_series), key=portfolio_value)

        summary_series.append((date,
                               observed_port_values[low_series_index],
                               observed_port_values[med_series_index],
                               observed_port_values[hi_series_index]))

    # Cache-friendly list rearrangement
    return { 'P10': [ (elem[0], elem[1]) for elem in summary_series ],
             'P50': [ (elem[0], elem[2]) for elem in summary_series ],
             'P90': [ (elem[0], elem[3]) for elem in summary_series ] }






