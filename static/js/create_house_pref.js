// render housechores if there are any in the database
$(document).ready(renderPhones(), renderHouseChores())

function addPhone(evt) {
	// function to add a phone number input

	// prevent any form submission
	evt.preventDefault();

	// create housemate count to add to ids and input names
	var housemate_count = ($('#phone-inputs span').length +1)

	// create new input element for a housemate phone number
	var new_phone_input = $('<input>').attr({
		name: 'housemate_phone' + +housemate_count,
		id: 'housemate_phone' + +housemate_count,
		placeholder: '+15105551234',
		type: 'text',
		required: true
	});

	// create new button element to remove phones and put an eventlistener on it
	var remove_phone_button = $('<button>').attr('name', 'remove_phone_button').html("Remove").on('click', removePhone)

	// add the new input element to the div right below admin phone
	$('#phone-inputs').append($('<span>').html('Housemate phone: '))
	// add the new input element to the div right below admin phone
	$('#phone-inputs').append(new_phone_input)
	// add the remove button next to the new phone input
	$('#phone-inputs').append(remove_phone_button)
	// add a break after each phone input
	$('#phone-inputs').append($('<br>'))

	// count number of housemates and put in hidden input
	$('#housemate_count').val($('#phone-inputs span').length)
}

// event listener for add phone button to create a new input field
$("#add-phone-button").on('click', addPhone)

function removePhone(evt) {
	// remove phone input
	evt.preventDefault();

	var rPButton = $(this); // the remove <button> element
	var remove_phone_input = rPButton.prev(); // the input field we wnat to remove
	var remove_phone_input_text = remove_phone_input.prev(); // the text we want to remove
	var remove_br = rPButton.next(); // the break after each phone input line

	// // re-calculate housemate numbering in the ui and input field names
	// if (rPButton.next().prop('tagName') === 'BR') {

	// 	var prev_count = $('#phone-inputs span').length

	// 	alert("this is the number of inputs: " + +prev_count)
	// 	// for each span after rPButton:
	// 	// 	update span_s housemate_count
	// 	// for each input after rPButton:
	// 	// 	update input name
	// }

	// remove it when remove button is clicked
	remove_phone_input.remove();
	remove_phone_input_text.remove();
	rPButton.remove();
	remove_br.remove();



	// re-count number of housemates and put in hidden input
	// $('#housemate_count').val($('#phone-inputs span').length)
}

function selectChore(evt) {
	// function to add chore-potential elements to the chore-selected table with a modal link
	var chore = $(evt.target);

	// if we've already moved this to being selected, don't do it again
	if (chore.hasClass('moved')) {
		return;
	};
	chore.addClass('moved');
	chore.attr('name', chore.html())

	// add click event listener on modal window link that will call a choreModal
	var choreElement = $('<a>').html(chore.html()).on('click', choreModal);
	choreElement.attr({
		href: '#',
		'data-target': '#myModal',
		'data-toggle': 'modal',
		id: chore.html()
	});
	$("#chore-selected").append($('<li>').html(choreElement));

	// created remove button for chore selected
	var liElement = $("#"+chore.html()).parent() // get li element of chore
	
	liElement.append($('<button>').attr('name', 'remove_chore_button').html("Remove").on('click', removeChore))

	// count the number of chore selected inputs 
	var hiddenChoreInput_count = ($('#chore-selected-inputs input').length +1)

	var hiddenChoreInput = $('<input>').attr({
		name: 'chores' + +hiddenChoreInput_count,
		id: 'hidden'+chore.html(),
		value: chore.html(),
		type: 'text'
	});

	$("#chore-selected-inputs").append(hiddenChoreInput);

	$("#hidden_count_of_chores").val(hiddenChoreInput_count)
}

// event listener for when user clicks on chore-potentials
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
	// passes chore frequency data from the modal window to the main form page
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

// event listener for when user submits modal window changes
$("#chore-freq-form").on('submit', passChoreFreq);

function removeChore(evt) {
	// removes chore from selected chores
	evt.preventDefault();

	var rCButton = $(this); // the remove <button> element
	var chore_a_tag = rCButton.prev() //this is the a tag 
	var rCChore = chore_a_tag.attr('id') // this is the name of the chore
	var remove_chore = chore_a_tag.parent(); // the li chore tag we want to remove
	var remove_hidden_chore = $('#hidden'+rCChore) //the hidden input tag

	// remove it when remove button is clicked
	rCButton.remove();
	remove_chore.remove();
	remove_hidden_chore.remove();

	// remove the styling on previously selected chores in chore-potentials and allow for re-select
	var changedChorePotential = $("[name|='"+rCChore+"']")
	changedChorePotential.removeClass('moved')
};

function renderPhones() {
	// function to add same click events to dom originating elements
	// that come from the database when schedule is already created

	// create housemate count to add to ids and input names
	var housemate_count = ($('#phone-inputs span').length +1)	

	// count number of housemates and put in hidden input
	$('#housemate_count').val($('#phone-inputs span').length)

	// add event listener to remove_phone_button for dom originating elements
	$('button[name="remove_phone_button"]').on('click', removePhone)


}

function renderHouseChores() {
	// function to add same click events to dom originating elements
	// that come from the database when schedule is already created

	// count the number of chore selected inputs 
	var hiddenChoreInput_count = ($('#chore-selected-inputs input').length)

	// add it to the hidden count of chores input
	$("#hidden_count_of_chores").val(hiddenChoreInput_count)

	// add the moved class for all housechores
	// need to do this


	// event listener for when dom originating housechores are clicked
	$(".housechore").on('click', choreModal)

	// add event listener for dom originating chores
	$("button[name='remove_chore_button']").on('click', removeChore)
}





