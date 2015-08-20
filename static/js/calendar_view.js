// when the document is finished loading, ajax request house chore data
var arrayOfEvents = []	;
$(document).ready(
	function() {
		// query the database first and return an array of ojects of the chores
		
		// start
		// $.when(
		// end
			$.ajax({
				url: '/render_house_chores', 
				method: "POST",
				success: function(result) {
					// reparse the results from json from object {date: (chore name, username, is_done, id)}
					// to array of object [{date: date, chore: chore, etc}, {date:date, chore: chore, etc}]
					console.log(result)

					// for each date of chores in the house
					for (var user_chore_date in result) {
						console.log("user_chore_date: " + user_chore_date);
						console.log("result[user_chore_date]: " + result[user_chore_date]);

						$('#user_chores').append($('<li>').html(user_chore_date));

						// for each user_chore tuple in the object
						for (var user_chore in result[user_chore_date]) {
							$('#user_chores').append($('<ul>').html(
								$('<li>').html(
									result[user_chore_date][user_chore].slice(0,3)))); 
							console.log("result[user_chore_date][user_chore].slice(0,3): " + result[user_chore_date][user_chore].slice(0,3))
							// for some reason is not displaying when 'false', fix this
							console.log("result[user_chore_date][user_chore][3]: " + result[user_chore_date][user_chore][3]) // returns id
							// result[user_chore_date][user_chore] is each chore tuple (chore name, username, is_done, id)

							// format object into array of event objects to inject into calendar
							arrayOfEvents.push({
								date: user_chore_date, 
								chore: result[user_chore_date][user_chore][0], 
								assignedTo: result[user_chore_date][user_chore][1],
								done: result[user_chore_date][user_chore][2],
								choreId: result[user_chore_date][user_chore][3]
							});
						}
						console.log("arrayOfEvents30" + arrayOfEvents)
						console.log(arrayOfEvents[0])
					};
					renderCalendar(arrayOfEvents)
				}
			})		
		// when the array is created, call the calendar function and pass it the events
		
		//start
		// ).done(
		//end
		// start
			// function(arrayOfEvents) {	
			// 	console.log(arrayOfEvents)
			// 	$('#calendar').clndr({
			// 		template: $('#calendar-template').html(),
			// 		events: [arrayOfEvents],	
			// 		clickEvents: {
			// 			click: function(target) {
			// 				console.log(target);
			// 				$(target.element).toggleClass('selected_day');
			// 				if ($(target.element).hasClass('selected_day')) {
			// 					alert("you selected_day")
			// 					alert("target.events[0]" + target.events[0].date + target.events[0].title) // gets first event's date & title
			// 					alert("target.date._i" + target.date._i) // this is the date in format YYYY-MM_DD
			// 					// $('#render-house-chores').append(target.events)
			// 				}
			// 			},
			// 			onMonthChange: function(month) {
			// 				console.log('you just went to ' + month.format('MMMM, YYYY'));
			// 			}
			// 		},
			// 		doneRendering: function() {
			// 			console.log('this would be a fine place to attach custom event handlers.');
			// 		}
			// 	});
			// }
		// end
		// start
		// )
		// end
	}
		
)


function renderCalendar(data){
	$('#calendar').clndr({
		template: $('#calendar-template').html(),
		events: data,
		clickEvents: {
			click: function(target) {
				console.log(target);
				$(target.element).toggleClass('selected_day');
				if ($(target.element).hasClass('selected_day')) {
					alert("you selected_day")
					alert("target.events[0]" + target.events[0].date + target.events[0].title) // gets first event's date & title
					alert("target.date._i" + target.date._i) // this is the date in format YYYY-MM_DD
					// $('#render-house-chores').append(target.events)
				}
			},
			onMonthChange: function(month) {
				console.log('you just went to ' + month.format('MMMM, YYYY'));
			}
		},
		doneRendering: function() {
			console.log('this would be a fine place to attach custom event handlers.');
		}
	});
}
