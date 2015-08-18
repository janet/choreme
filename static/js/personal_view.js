$(document).ready(function() {
	$.post('/render_personal_chores', function(result) {
		console.log(result)

		for (var user_chore in result) {
			console.log(result[user_chore])

			var pc_count = ($('#personal_chores li').length +1)
			
			$('#personal_chores').append($('<li>').html(
				user_chore + ': ' + 
				result[user_chore][0][0] + ': ' + 
				result[user_chore][0][1]
			));

			$('#personal_chores').append($('<input>').attr({
				name: 'pc' + +pc_count,
				id: 'pc' + +result[user_chore][0][2], // this is the user_chore.id
				type: 'checkbox',
				value: result[user_chore][0][2]
			}));
		}
	});
});