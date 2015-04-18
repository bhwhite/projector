import datetime
from bottle import route, run, static_file
from engine import asset, holding, portfolio, portfolio_generator, return_sampler, simulator

@route('/static/<path:path>')
def handle_static(path):
    return static_file(path, root='/Users/bwhite/projector/git/projector/src/static')

@route('/')
def handle_index():
    user_supplied_total_value = 1000
    user_supplied_portfolio_generator = 'Fixed Composition: 80% Stocks / 20% Bonds'
    user_supplied_return_sampler = 'Constant 6% Annual'
    user_supplied_sim_start_date = datetime.date(2015, 4, 18)
    user_supplied_sim_end_date = datetime.date(2030, 12, 31)
    user_supplied_sample_start_date = datetime.date(1960, 1, 1)
    user_supplied_sample_end_date = datetime.date(2015, 4, 18)
    
    output = []

    holdings = [ holding.Holding(asset.ASSETS['CASH'], user_supplied_total_value), ]
    asset_states = [ asset.AssetState(1.0), ]

    cur_portfolio = portfolio.Portfolio(holdings, asset_states)
    cur_portfolio_generator = portfolio_generator.PORTFOLIO_GENERATORS[user_supplied_portfolio_generator]()
    cur_return_sampler = return_sampler.RETURN_SAMPLERS[user_supplied_return_sampler](cur_portfolio_generator,
                                                                                      user_supplied_sample_start_date,
                                                                                      user_supplied_sample_end_date)

    results = simulator.simulate(cur_return_sampler,
                                 cur_portfolio_generator,
                                 cur_portfolio,
                                 user_supplied_sim_start_date,
                                 user_supplied_sim_end_date)

    output.append('<br>{}</br>'.format(str(cur_portfolio).replace('<','').replace('>','')))
    output.append('<br>{}</br>'.format(str(cur_portfolio_generator).replace('<','').replace('>','')))
    output.append('<br>{}</br>'.format(str(cur_return_sampler).replace('<','').replace('>','')))

    output.append(str(results))

    output.append('\n'.join(['<li>{}</li>'.format(pg) for pg in portfolio_generator.PORTFOLIO_GENERATORS]))
    return '\n'.join(output)

run(host='localhost', port=8081, debug=True)
