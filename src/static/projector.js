
function show_chart_click_handler(event)
{
    var current_portfolio_value = $('#current_portfolio_value').val();
    parsed_value = parseFloat(current_portfolio_value)
    if (isNaN(parsed_value))
    {
	$('#current_portfolio_error').text('Unable to parse ' + current_portfolio_value);
    }
}

$(document).ready(
    function()
    {
	$(document).on('click', '#show_chart_button', {}, show_chart_click_handler);
    }
);
