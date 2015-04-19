
function add_contribution_click_handler(event)
{
    comments = [ 'Time to save!', 'Crank up the savings!' ]
    
    // var item = items[Math.floor(Math.random()*items.length)];

    $('#projector_form').append('<div class="row"><div class="small-4">' +
				comments[Math.floor(Math.random() * comments.length)]
				+ ' This is a ' +
				'</div><div class="small-4 end">' +
				'<select>' +
				'<option value="Daily">Daily</option>' +
				'<option value="Weekly">Weekly</option>' +
				'</select>' +
				' contribution of ' +
				'<input type="text" name="current_portfolio_value" placeholder="0.00" value="0.00"/>' + 
				'</div></div>');
}

$(document).ready(
    function()
    {
	$(document).on('click', '#add_contribution', {}, add_contribution_click_handler);
    }
);
