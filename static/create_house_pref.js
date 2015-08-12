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

	//create new button element to remove phones and put an eventlistener on it
	var remove_phone_button = $('<button>').attr('name', 'remove_phone_button').html("Remove").on('click', removePhone)

	//add the new input element to the div right below admin phone
	$('#phone-inputs').append($('<span>').html('Housemate phone: '))
	//add the new input element to the div right below admin phone
	$('#phone-inputs').append(new_phone_input)
	//add the remove button next to the new phone input
	$('#phone-inputs').append(remove_phone_button)
	//add a break after each phone input
	$('#phone-inputs').append($('<br>'))
}

function removePhone(evt) {
	evt.preventDefault();

	var rPButton = $(this); // the remove <button> element
	var remove_phone_input = rPButton.prev(); // the input field we wnat to remove
	var remove_phone_input_text = remove_phone_input.prev(); // the text we want to remove
	var remove_br = rPButton.next(); // the break after each phone input line

	//remove it when remove button is clicked
	remove_phone_input.remove();
	remove_phone_input_text.remove();
	rPButton.remove();
	remove_br.remove();

}

$("#add-phone-button").on('click', addPhone)
function selectChore(evt) {
	// function to add chore-potential elements to the chore-selected table with a modal link
	var chore = $(evt.target);

	// if we've already moved this to being selected, don't do it again
	if (chore.hasClass('moved')) {
		return;
	}
	chore.addClass('moved');

	// add click event listener on modal window link that will call a choreModal
	var choreElement = $('<a>').html(chore.html()).on('click', choreModal);
	choreElement.attr({
		href: '#',
		'data-target': '#myModal',
		'data-toggle': 'modal',
		id: chore.html()
	});
	$("#chore-selected").append($('<li>').html(choreElement));

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

	var selectedChore = $(evt.target).attr('id'); // the <a> tag id which is the chore name

	var modal = $('#myModalLabel');

	var hidden_modal_input = $('#hidden-modal-chore')

	hidden_modal_input.val(selectedChore); // set hidden modal window input to the chore name
	modal.html(selectedChore); // set modal window title to chore name
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

