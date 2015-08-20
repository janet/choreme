$(document).ready(function() {
	$.post('/render_house_chores', function(result) {
		console.log(result)

		for (var user_chore_date in result) {
			console.log("user_chore_date: " + user_chore_date);
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

				// format object into array of event objects to inject into calendar
				var arrayOfEvents = []
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

		// call calendar with a function so that it happens after the arrayOvEvents are created
		createCalendar();

		
	});
});

function createCalendar() {
	$('#calendar').clndr({
		  template: $('#calendar-template').html(),
		  events: 
		  // arrayOfEvents,
		  [
			    { date: '2015-08-09', title: 'CLNDR GitHub Page Finished', url: 'http://github.com/kylestetz/CLNDR' },
			     {date: "2015-08-30", chore: "Dusting", assignedTo: null, done: false, choreId: 19}
			  ],
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

// console.log("arrayOfEvents36" + arrayOfEvents)

// $('#calendar').clndr({
//   template: $('#calendar-template').html(),
//   events: arrayOfEvents,
//   clickEvents: {
//     click: function(target) {
//       console.log(target);
//       $(target.element).toggleClass('selected_day');
//       if ($(target.element).hasClass('selected_day')) {
//       	alert("you selected_day")
//       	alert("target.events[0]" + target.events[0].date + target.events[0].title) // gets first event's date & title
//       	alert("target.date._i" + target.date._i) // this is the date in format YYYY-MM_DD
//       	// $('#render-house-chores').append(target.events)
//       }
//     },
//     onMonthChange: function(month) {
//       console.log('you just went to ' + month.format('MMMM, YYYY'));
//     }
//   },
//   doneRendering: function() {
//     console.log('this would be a fine place to attach custom event handlers.');
//   }
// });


// $.post('/render_house_chores', function(result){
// 	for (var user_chore_date in result) {
// 		var calClassName = ".calendar-day-".concat(user_chore_date)
// 		$(calClassName).on('click', )
// 	}
// })

	