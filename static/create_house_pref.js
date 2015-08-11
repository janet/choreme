function selectChore(evt) {
	// function to add chore-potential elements to the chore-selected table with a modal link
	var chore = $(evt.target);

	// if we've already moved this to being selected, don't do it again
	if (chore.hasClass('moved')) {
		return;
	}
	chore.addClass('moved');
	var choreElement = $('<a>').html(chore.html()).on('click', choreModal);
	choreElement.attr({
		href: '#',
		'data-target': '#myModal',
		'data-toggle': 'modal',
		id: chore.html()
	});
	$("#chore-selected").append(choreElement);
	$("#chore-selected-inputs").append('<input type="text" name="chores" value="' + chore.html() + '">');
}


$("#chore-potentials li").on('click', selectChore);

function choreModal(evt) {
	// function to create modal window for each chore that is selected

	var selectedChore = $(evt.target); // the <a> tag
	var modal = $('#myModalLabel');

	var hidden_chore_input = $('#hidden-chore')

	hidden_chore_input.val(selectedChore.html()); // set hidden modal window input to the chore name
	modal.html(selectedChore.html()); // set modal window title to chore name
}

function setChoreFreq(evt) {
	evt.preventDefault();

	$.post("/save_chore_freq",
		$('#chore-freq-form').serialize(),
		function(result) {
			$('')
		})
}