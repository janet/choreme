// when the document is finished loading, ajax request house chore data
var arrayOfEvents = [];
$(document).ready(
	function() {
		// query the database first and return an array of objects of the chores
		$.ajax({
			url: '/render_house_chores', 
			method: "POST",
			success: function(result) {
				// reparse the results from json from object {date: [chore name, username, is_done, id]}
				// to array of object [{date: date, chore: chore, etc}, {date:date, chore: chore, etc}]
				// console.log(result)

				// for each date of chores in the house
				for (var user_chore_date in result) {
					// console.log("user_chore_date: " + user_chore_date);
					// console.log("result[user_chore_date]: " + result[user_chore_date]);

					// $('#user_chores').append($('<li>').html(user_chore_date));

					// for each user_chore tuple in the object
					for (var user_chore in result[user_chore_date]) {
						// $('#user_chores').append($('<ul>').html(
						// 	$('<li>').html(
						// 		result[user_chore_date][user_chore].slice(0,3)))); 
						// console.log("result[user_chore_date][user_chore].slice(0,3): " + result[user_chore_date][user_chore].slice(0,3))
						// for some reason is not displaying when 'false', fix this
						// console.log("result[user_chore_date][user_chore][3]: " + result[user_chore_date][user_chore][3]) // returns id
						// result[user_chore_date][user_chore] is each chore tuple (chore name, username, is_done, id)

						// format object into array of event objects to inject into calendar
						arrayOfEvents.push({
							date: user_chore_date, 
							chore: result[user_chore_date][user_chore][0], 
							assignedTo: result[user_chore_date][user_chore][1],
							is_done: result[user_chore_date][user_chore][2],
							choreId: result[user_chore_date][user_chore][3]
						});
					}
					// console.log("arrayOfEvents30" + arrayOfEvents)
					// console.log(arrayOfEvents[0])
				};
				renderCalendar(arrayOfEvents)
			}
		})		
	}
		
)


function renderCalendar(data){
	// create a calendar instance and pass it the database queried events
	var myCalendar = $('#calendar').clndr({
		template: $('#calendar-template').html(),
		events: data,
		clickEvents: {
			click: function(target) {
				console.log(target);
				// remove the gray highlight from any other selected calendar days on click
				$('.selected-day').removeClass('selected-day');

				// reset the chores that display on click
				$('#render-house-chores').html("");

				// add the gray highlight on click
				$(target.element).toggleClass('selected-day');

				// when user clicks on a day, render the assigned chores
				if ($(target.element).hasClass('selected-day')) {
					for (var rcEventsIndex in target.events){
						// create a table to put the chores to render on day click
						var rcChoreDiv = $('<tr>');

						// put the chore, assignedTo and is_done in the div
						rcChoreDiv.html(
							'<td>' +
								target.events[rcEventsIndex].chore + 
							'</td>' +
							'<td>' +
								target.events[rcEventsIndex].assignedTo + 
							'</td>' +
							'<td>' +
								doneLookup[target.events[rcEventsIndex].is_done] +
							'</td>'
							)

						$('#render-house-chores').append(rcChoreDiv)
					}
					$('#render-house-chores').prepend(
						'<tr>' +
							'<th>Chore</th>' +
							'<th>Assigned</th>' +
							'<th>Done</th>' +
						'</tr>'
						)
				}
			},
			onMonthChange: function(month) {
				console.log('you just went to ' + month.format('MMMM, YYYY'));
			}
		},
		doneRendering: function() {
			// add css class to days with events
			for (var eventIndex in this.eventsThisInterval){
				$('.calendar-day-'+this.eventsThisInterval[eventIndex].date).addClass('event-day')
				// console.log('/static/img/'+this.eventsThisInterval[eventIndex].chore+'.png')
				$('.calendar-day-'+this.eventsThisInterval[eventIndex].date).append(
					$('<img>').attr('src', '/static/img/'+this.eventsThisInterval[eventIndex].chore+'.png').
						addClass('img-format'))
			}
			// add vertical alignment to all calendar cells
			$('.day').attr('valign','top');
		}
	});
}

var doneLookup = {true: "Done", false: "Not Yet"}

