$(document).ready(function() {
	/*
		This function checks whether two teams have been chosen from the dropdown menus.
		If two teams have been chosen, then it brings up the "Trade Options" stuff, and
		then handles how a player is moved to the other team when it is clicked on.
	*/
	var readyToTrade = function() {
		var dropdown1text = $('#dropdownMenuButton1').text()
		var dropdown2text = $('#dropdownMenuButton2').text()
		var dropdown3text = $('#dropdownMenuButton3').text()

		if (dropdown1text !== 'Choose team' && dropdown2text !== 'Choose team'
			|| dropdown2text !== 'Choose team' && dropdown3text !== 'Choose team'
			|| dropdown1text !== 'Choose team' && dropdown3text !== 'Choose team') {

			if(dropdown1text===dropdown2text){
				//if  any two  dropdown contains same team then no action
				return ;
			}else if(dropdown2text===dropdown3text){
				//if  any two  dropdown contains same team then no action
				return ;
			}else if(dropdown1text===dropdown3text){
				//if  any two  dropdown contains same team then no action
				return ;
			}

			// We bring the "Trade Options" part up here
			var team1Div = $('#team1');
			//$("#team1tradeoptions").toggleClass('d-none d-block');
			$("#team1tradeoptions").addClass('d-block');
			var team2Div = $('#team2');
			//$("#team2tradeoptions").toggleClass('d-none d-block');
			$("#team2tradeoptions").addClass('d-block');

			var team3Div = $('#team3');
			//$("#team3tradeoptions").toggleClass('d-none d-block');
			$("#team3tradeoptions").addClass('d-block');


			// When a player is clicked, they are transferred to the other team and put
			// under "Trade Options"
			$("#teamplayers1").click(function(event) {
				var player = event.target;
				$(player).appendTo("#team2tradeoptions div")

				var allteam1options = $("#team1tradeoptions div").children();
				var allteam2options = $("#team2tradeoptions div").children();

				var currentteam1players = []
				var currentteam2players = []

				if (allteam1options.length === 1 && allteam2options.length === 1) {
					team1options_playername = $(allteam1options[0]).text();
					team2options_playername = $(allteam2options[0]).text();

					if (team1options_playername === "Daniel Theis" && team2options_playername === "Kent Bazemore") {
						console.log("worked");
					}
				}
			});
			// $("#teamplayers2").click(function(event) {
			// 	var player = event.target;
			// 	$(player).appendTo("#team1tradeoptions div");

			// 	var allteam1options = $("#team1tradeoptions div").children();
			// 	var allteam2options = $("#team2tradeoptions div").children();

			// 	if (allteam1options.length === 1 && allteam2options.length === 1) {
			// 		team1options_playername = $(allteam1options[0]).text();
			// 		team2options_playername = $(allteam2options[0]).text();

			// 		if (team1options_playername === "Daniel Theis" && team2options_playername === "Kent Bazemore") {
			// 			$("#testtradeNotSuccessful").toggleClass('d-none d-block');
			// 			$("#testtrade").toggleClass('d-block d-none');
			// 		}
			// 	}
			// });

			// // This handles clicking a player in "Trade Options" and puts them back
			// $("#team1tradeoptions div").click(function(event) {
			// 	var player = event.target;
			// 	$("#teamplayers2").prepend(player);
			// });
			// $("#team2tradeoptions div").click(function(event) {
			// 	var player = event.target;
			// 	$("#teamplayers1").prepend(player);
			// });

			// // This is just putting the Test Trade button
			// $("#testtrade").toggleClass('d-none d-block');
		}
	};


	// This handles what happens when each dropdown is clicked			
	$('.team1dropdown').click(function() {

		// This makes the dropdown button have the text of the team
		var teamSelected = $(this).text();
		$('#dropdownMenuButton1').text(teamSelected);
		readyToTrade();
	});
	$('.team2dropdown').click(function() {

		// This makes the dropdown button have the text of the team
		var teamSelected = $(this).text();
		$('#dropdownMenuButton2').text(teamSelected);
		readyToTrade();
	});
	$('.team3dropdown').click(function() {

		// This makes the dropdown button have the text of the team
		var teamSelected = $(this).text();
		$('#dropdownMenuButton3').text(teamSelected);
		readyToTrade();
	});
});