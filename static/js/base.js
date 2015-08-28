$(document).ready(renderTabActive)

function renderTabActive() {
	// function to be called on page load to render tabs active 
	// if applicable

	var pathname = window.location.pathname

	if (pathname === '/personal_view') {
		$('#personal_tab').addClass('active')
	}
	if (pathname === '/calendar_view') {
		$('#calendar_tab').addClass('active')
	}
	if (pathname === '/create_house_pref') {
		$('#house_pref_tab').addClass('active')
	}

}
