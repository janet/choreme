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
	});
	$("#chore-selected").append(choreElement);

	var hiddenChoreInput = $('<input>').attr({
		name: 'chores',
		id: chore.html(),
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
	$('#myModal').modal('hide')

	// get the chore name from the modal window hidden input
	var hiddenModalChore = $('#hidden-modal-chore').val();

	// ajax send modal window form to main form
	$.post("/save_chore_freq",
		$('#chore-freq-form').serialize(),
		function(result) {
			$('#'+hiddenModalChore).val(
				result.chore_name + '|' + result.week_freq + '|' + result.day)
		})
}


$("#chore-freq-form").on('submit', passChoreFreq);
