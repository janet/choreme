$(document).ready(function() {
	$.post('/render_house_chores', function(result) {
		console.log(result)

		for (var user_chore_date in result) {
			console.log("user_chore_date: " + user_chore_date)
			console.log("result[user_chore_date]: " + result[user_chore_date]);
			$('#user_chores').append($('<li>').html(user_chore_date));
			for (var user_chore in result[user_chore_date]) {
				$('#user_chores').append($('<ul>').html($('<li>').html(result[user_chore_date][user_chore])));
				console.log("result[user_chore_date][user_chore]: " + result[user_chore_date][user_chore]) 
				// result[user_chore_date][user_chore] is each chore tuple (chore name, username, is_done)
			}
		};
	});
});


	