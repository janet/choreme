$(document).ready(function() {
	$.post('/render_house_chores', function(result) {
		console.log(result)

		for (var user_chore_date in result) {
			console.log("user_chore_date: " + user_chore_date)
			console.log("result[user_chore_date]: " + result[user_chore_date]);
			$('#user_chores').append($('<li>').html(user_chore_date));
			for (var user_chore in result[user_chore_date]) {
				$('#user_chores').append($('<ul>').html(
					$('<li>').html(
						result[user_chore_date][user_chore].slice(0,3)))); 
				console.log("result[user_chore_date][user_chore].slice(0,3): " + result[user_chore_date][user_chore].slice(0,3))
				// for some reason is not displaying when 'false', fix this
				console.log("result[user_chore_date][user_chore][3]: " + result[user_chore_date][user_chore][3]) // returns id
				// result[user_chore_date][user_chore] is each chore tuple (chore name, username, is_done, id)
			}
		};
	});
});


	