$(document).ready(function() {
	$.post('/render_personal_chores', function(result) {
		console.log(result)

		for (var user_chore in result) {
			console.log(result[user_chore])

			var pc_count = ($('#personal_chores li').length +1)
			
			// create list element for each chore
			$('#personal_chores').append($('<li>').html(
				user_chore + ': ' + 
				result[user_chore][0][0] + ': ' + // chore name
				result[user_chore][0][1] // chore is_done
			));

			// create checkbox input after each chore list element
			$('#personal_chores').append($('<input>').attr({
				name: 'pc' + +pc_count,
				id: result[user_chore][0][2], // user_chore.id
				type: 'checkbox',
				value: result[user_chore][0][2], // user_chore.id
			}));		

			// if is_done is false, checkbox should not be checked, otherwise check it
			if (result[user_chore][0][1] === false) {
				$('#' + +result[user_chore][0][2])[0].checked = false;
			}
			else {
				$('#' + +result[user_chore][0][2])[0].checked = true;
			}

			// when the checkbox is checked / unchecked do stuff
			$('#'+ +result[user_chore][0][2]).change(function(){

			    if($(this).is(':checked'))
			    {
			        alert("checked");
			        $('#hidden_personal_chore_input').val($(this).attr('id'));
			        $.post("/chore_done",
			        	$('#chore_done').serialize(),
			        	function(result){
			        		alert("updated database with checked");
			    		})
			   	}	
			    else
			    {
			    	alert("unchecked");
			        $('#hidden_personal_chore_input').val($(this).attr('id'));
			    	$.post("/chore_undone",
			        	$('#chore_done').serialize(),
			        	function(result){
			        		alert("updated database with unchecked");
			    		})
			    }    

			});
		}
	});
});

