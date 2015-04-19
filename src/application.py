import datetime
import pickle
import json

from bottle import redirect, request, route, run, static_file
from engine import asset, holding, output_formatters, portfolio, portfolio_generator, return_sampler, simulator

#all_returns = pickle.load(open('all-returns.pkl', 'rb'))
#return_sampler.HISTORICAL_RETURNS = all_returns

@route('/static/<path:path>')
def handle_static(path):
    return static_file(path, root='static')

index_output = """
<!doctype html>
<html class="no-js" lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/foundation/5.5.1/css/foundation.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/projector.css" />

    <title>Projector</title>
  </head>
  <body>
    <div class="row">
      &nbsp;
    </div>

    <div class="row">
      <div class="small-5 columns">
        <img src="/static/logo.png">
      </div>
<!--    </div>

    <p />

    <div class="row"> -->

      <div class="small-5 columns">

        <!-- <form method="post" id="projector_form" action="/"> -->
        <form id="projector_form">
          <div class="row">
            <div class="small-12 columns">
                <label>
                  <span data-tooltip aria-haspopup="true" class="has-tip round" title="If you're starting from scratch, no worries. You can leave this set to 0.00.">How big is your portfolio today?</span> <font color="red" id="current_portfolio_error"></font>
                  <input type="text" id="current_portfolio_value" name="current_portfolio_value" placeholder="0.00" value="0.00"/>
                </label>
             </div>
          </div>
          <div class="row">
            <div class="small-12 columns">
               <label>
                  <span data-tooltip aria-haspopup="true" class="has-tip round" title="What kind of portfolio would you like to hold?">Portfolio choices:</span>
                 <select id="desired_portfolio_generator" name="desired_portfolio_generator">
                   {}
                 </select>
               </label>  
             </div>
          </div>

          <div class="row">
            <div class="small-12 columns">
                <label>
                  <span data-tooltip aria-haspopup="true" class="has-tip round" title="You can do it! Start small, grow big!">How much will you save monthly?</span> <font color="red" id="monthly_investment_error"></font>
                  <input type="text" id="monthly_investment" name="monthly_investment" placeholder="0.00" value="0.00"/>
                </label>
             </div>
          </div>

          <div class="row">
            <div class="small-12 columns">
                <label>
                  <span data-tooltip aria-haspopup="true" class="has-tip round" title="Goals are good!">What's your target value?</span> <font color="red" id="goal_error"></font>
                  <input type="text" id="goal" name="goal" placeholder="0.00" value="0.00"/>
                </label>
             </div>
          </div>

          <a href="#" class="button round" id="show_chart_button">Show me the charts!</a>
          <!-- <input type="submit" value="Show me the charts!" id="show_chart_button" name="submit" class="button round"> -->

        </form>

      </div>

    </div>

    <div class="row">
      <div class="small-12 columns"
        <div id="chart_section" style="height: 420px; min-width: 310px"></div>
      </div>
    </div>

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="http://code.highcharts.com/stock/highstock.js"></script>
    <script src="http://code.highcharts.com/stock/modules/exporting.js"></script>
    <script type="text/javascript" src="http://cdn.foundation5.zurb.com/foundation.js"></script>
    <script>
      $(document).foundation();
    </script>
    <script type="text/javascript" src="/static/projector.js"></script>

  </body>
</html>
"""

def handle_index_post():
    try:
        current_portfolio_value = request.forms.get('current_portfolio_value')
        desired_portfolio_generator = request.forms.get('desired_portfolio_generator')
        monthly_investment = request.forms.get('monthly_investment')

        if not current_portfolio_value or not desired_portfolio_generator or not monthly_investment:
            redirect('/')

        current_portfolio_value = float(current_portfolio_value)
        monthly_investment = float(monthly_investment)
    except Exception, e:
        redirect('/')

    return ', '.join([str(current_portfolio_value), str(desired_portfolio_generator), str(monthly_investment)])

def handle_index_get():
    def format_portfolio_generators():
        portfolio_generators = sorted(portfolio_generator.PORTFOLIO_GENERATORS.keys())
        return '\n'.join( [ '<option value="{}">{}</option>'.format(pg, pg) for pg in portfolio_generators ] )

    output = index_output.format(format_portfolio_generators())

    return output

def handle_getdata_get():
    user_supplied_sim_start_date = datetime.date(2015, 4, 18)
    user_supplied_sim_end_date = datetime.date(2030, 12, 31)
    user_supplied_sample_start_date = datetime.date(1990, 1, 1)
    user_supplied_sample_end_date = datetime.date(2015, 4, 18)

    user_supplied_total_value = float(request.query.current_portfolio_value)
    user_supplied_portfolio_generator = request.query.desired_portfolio_generator
    user_supplied_monthly_investment = float(request.query.monthly_investment)
    user_supplied_goal_value = request.query.goal_value
    user_supplied_return_sampler = 'Historical Returns'

    try:
        goal_value = float(goal_value)
    except:
        goal_value = 0.0

    holdings = [ holding.Holding(asset.ASSETS['CASH'], user_supplied_total_value), ]
    asset_states = [ asset.AssetState(1.0), ]

    cur_portfolio = portfolio.Portfolio(holdings, asset_states)
    cur_portfolio_generator = portfolio_generator.PORTFOLIO_GENERATORS[user_supplied_portfolio_generator]()
    cur_return_sampler = return_sampler.RETURN_SAMPLERS[user_supplied_return_sampler](cur_portfolio_generator,
                                                                                      user_supplied_sample_start_date,
                                                                                      user_supplied_sample_end_date)

    all_results = [ simulator.simulate(cur_return_sampler,
                                       cur_portfolio_generator,
                                       cur_portfolio,
                                       user_supplied_sim_start_date,
                                       user_supplied_sim_end_date,
                                       user_supplied_monthly_investment * 12.0)
                    for ii in range(30) ]
    formatted_output = json.dumps(output_formatters.highcharts_series(all_results))
    # print '---\n{}\n---'.format(formatted_output)
    return formatted_output

@route('/foo')
def handle_foo():
    user_supplied_total_value = 1000
    user_supplied_portfolio_generator = 'Aggressive: 100% Stocks'
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

route('/', method='GET')(handle_index_get)
route('/getdata', method='GET')(handle_getdata_get)
route('/', method='POST')(handle_index_post)

run(host='localhost', port=8081, debug=True)

