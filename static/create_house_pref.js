function selectChore(evt) {
	// function to add chore-potential elements to the chore-selected table with a modal link
	var chore = $(evt.target);

	// if we've already moved this to being selected, don't do it again
	if (chore.hasClass('moved')) {
		return;
	}
	chore.addClass('moved');

	// add click event listener on modal window link that will call a choreModal
	var choreElement = $('<li>').html($('<a>').html(chore.html()).on('click', choreModal));
	choreElement.attr({
		href: '#',
		'data-target': '#myModal',
		'data-toggle': 'modal',
		id: chore.html()
	});
	$("#chore-selected").append(choreElement);

	var hiddenChoreInput = $('<input>').attr({
		name: 'chores',
		id: 'hidden'+chore.html(),
		value: chore.html()
	});
	$("#chore-selected-inputs").append(hiddenChoreInput);
}


$("#chore-potentials li").on('click', selectChore);

function choreModal(evt) {
	// function to populate modal window with that chore specific data

	var selectedChore = $(evt.target); // the <a> tag
	var modal = $('#myModalLabel');

	var hidden_modal_input = $('#hidden-modal-chore')

	hidden_modal_input.val(selectedChore.html()); // set hidden modal window input to the chore name
	modal.html(selectedChore.html()); // set modal window title to chore name
}

function passChoreFreq(evt) {
	evt.preventDefault();

	// close the modal window
	$('#myModal').modal('hide')

	// get the chore name from the modal window hidden input
	var hiddenModalChore = $('#hidden-modal-chore').val();

	// ajax send modal window form values to render in selected chores table
	$.post("/pass_chore_freq",
		$('#chore-freq-form').serialize(),
		function(result) {
			$('#'+hiddenModalChore).html(
				result.chore_name + '|' + result.week_freq + '|' + result.day)
		})

	// ajax send modal window form to main form
	$.post("/pass_chore_freq",
		$('#chore-freq-form').serialize(),
		function(result) {
			$('#hidden'+hiddenModalChore).val(
				result.chore_name + '|' + result.week_freq + '|' + result.day)
		})
}

$("#chore-freq-form").on('submit', passChoreFreq);


function addPhone(evt) {
	//function to add a phone number input

	//prevent any form submission
	evt.preventDefault();

	//create new input element for a housemate phone number
	var new_phone_input = $('<input>').attr({
		name: 'phones',
		placeholder: '+15105551234',
		type: 'text'
	});

	//add the new input element to the div right below admin phone
	$('#phone-inputs').append(new_phone_input)
}

$("#add-phone-button").on('click', addPhone)
