
// Replace the first element -- which is presumed to be a date string
// in the ISO format 'YYYY-MM-DD' -- with a JavaScript Date instance
function replaceDate(datapoint) {
    datapoint[0] = Date.parse(datapoint[0]);
    return datapoint;
}

function addAwesomeSeries(chart_document_id, series_plural) {
    series_plural = $.parseJSON(series_plural);
    var num_series = series_plural.length;

    for (var i = 0; i != num_series; i++)
    {
	// console.log(i + ': ' + series_plural[i]);
        series_plural[i].data = series_plural[i].data.map(replaceDate)
    }
    
    new Highcharts.Chart({
        chart: {
            renderTo: chart_document_id
        },
        xAxis: {
            type: 'datetime',
            title: { text: 'Date' }
        },
	yAxis: {
	    title: { text: 'Portfolio (dollars)' }
	},
	title: {
            text: "Portfolio Simultions"
	},
        series: series_plural
    });
}

function show_chart_click_handler(event)
{
    $('#current_portfolio_error').text('');
    $('#monthly_investment_error').text('');

    var current_portfolio_value = $('#current_portfolio_value').val();
    parsed_value = parseFloat(current_portfolio_value)
    if (isNaN(parsed_value))
    {
	$('#current_portfolio_error').text('Unable to parse ' + current_portfolio_value);
    }
    current_portfolio_value = parsed_value
    
    var monthly_investment = $('#monthly_investment').val();
    parsed_value = parseFloat(monthly_investment)
    if (isNaN(parsed_value))
    {
	$('#monthly_investment_error').text('Unable to parse ' + monthly_investment);
    }
    monthly_investment = parsed_value

    var goal_value = $('#goal').val();

    // alert(current_portfolio_value + ', ' + monthly_investment);

    var desired_portfolio_generator = $('#desired_portfolio_generator').val();

    var args =
	'current_portfolio_value=' + current_portfolio_value + '&' +
	'monthly_investment=' + monthly_investment + '&' +
	'goal_value' + goal_value + '&' +
	'desired_portfolio_generator=' + desired_portfolio_generator;
    // console.log(args);
    
    $.get("/getdata?" + args, function(input_data)
	  {
	      addAwesomeSeries('chart_section', input_data);
	  });
}

$(document).ready(
    function()
    {
	$(document).on('click', '#show_chart_button', {}, show_chart_click_handler);
    }
);
