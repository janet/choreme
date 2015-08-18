$(document).ready(function() {
	$.post('/render_personal_chores', function(result) {
		console.log(result)

		for (var user_chore in result) {
			console.log(result[user_chore])

			var pc_count = ($('#personal_chores li').length +1)
			
			$('#personal_chores').append($('<li>').html(
				user_chore + ': ' + 
				result[user_chore][0][0] + ': ' + // chore name
				result[user_chore][0][1] // chore is_done
			));

			$('#personal_chores').append($('<input>').attr({
				name: 'pc' + +pc_count,
				id: 'pc' + +result[user_chore][0][2], // user_chore.id
				type: 'checkbox',
				value: result[user_chore][0][2], // user_chore.id
			}));	

			// if is_done is false, checkbox should not be checked, otherwise it should be
			if (result[user_chore][0][1] === false) {
				$('#pc'+ +result[user_chore][0][2])[0].checked = false;
			}
			else {
				$('#pc'+ +result[user_chore][0][2])[0].checked = true;
			}
		}
		console.log("result[user_chore][0][1]" + result[user_chore][0][1])

		
	});
});