import datetime
from bottle import route, run, static_file
from engine import asset, holding, portfolio, portfolio_generator, return_sampler, simulator

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
      <div class="small-12 columns">
	LOGO GOES HERE
      </div>
    </div>

    <p />

    <div class="row">

      <div class="small-12">

        <form method="post" id="projector_form" action="/">
          <div class="row">
            <div class="small-6">
                <label>
                  <span data-tooltip aria-haspopup="true" class="has-tip round" title="If you're starting from scratch, no worries. You can leave this set to 0.00.">How big is your portfolio today?</span>
                  <input type="text" name="current_portfolio_value" placeholder="0.00" value="0.00"/>
                </label>
             </div>
          </div>
          <div class="row">
            <div class="small-6">
               <label>
                  <span data-tooltip aria-haspopup="true" class="has-tip round" title="What kind of portfolio would you like to hold?">Portfolio choices:</span>
                 <select name="desired_portfolio_generator">
                   {}
                 </select>
               </label>  
             </div>
          </div>
          <div class="row">
            <div class="small-6">
               <a href="#" class="button round" id="add_contribution">Add contribution</a>
             </div>
          </div>

        </form>

      </div>

    </div>

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://cdn.foundation5.zurb.com/foundation.js"></script>
    <script>
      $(document).foundation();
    </script>
    <script type="text/javascript" src="/static/projector.js"></script>

  </body>
</html>
"""

def handle_index_post():
    return ''

def handle_index_get():
    def format_portfolio_generators():
        portfolio_generators = sorted(portfolio_generator.PORTFOLIO_GENERATORS.keys())
        return '\n'.join( [ '<option value="{}">{}</option>'.format(pg, pg) for pg in portfolio_generators ] )

    output = index_output.format(format_portfolio_generators())

    return output

@route('/foo')
def handle_foo():
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

route('/', method='GET')(handle_index_get)
route('/', method='POST')(handle_index_post)

run(host='localhost', port=8081, debug=True)

