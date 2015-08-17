$(document).ready(function() {
	$.post('/render_personal_chores', function(result) {
		console.log(result)

		for (var user_chore in result) {
			console.log(result[user_chore])
			$('#personal_chores').append($('<li>').html(user_chore + ': ' + result[user_chore][0] + ': ' + result[user_chore][1]));
		}
	});
});