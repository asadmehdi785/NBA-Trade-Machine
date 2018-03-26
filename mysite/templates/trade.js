$(document).ready(function() {
	/*
		This function checks whether two teams have been chosen from the dropdown menus.
		If two teams have been chosen, then it brings up the "Trade Options" stuff, and
		then handles how a player is moved to the other team when it is clicked on.
	*/
	var readyToTrade = function() {
		var dropdown1text = $('#dropdownMenuButton1').text()
		var dropdown2text = $('#dropdownMenuButton2').text()
		if (dropdown1text !== 'Choose team' && dropdown2text !== 'Choose team') {

			// We bring the "Trade Options" part up here
			var team1Div = $('#team1');
			$("#team1tradeoptions").toggleClass('d-none d-block');
			var team2Div = $('#team2');
			$("#team2tradeoptions").toggleClass('d-none d-block');

			// When a player is clicked, they are transferred to the other team and put
			// under "Trade Options"
			$("#teamplayers1").click(function(event) {
				var player = event.target;
				$(player).appendTo("#team2tradeoptions div")
			});
			$("#teamplayers2").click(function(event) {
				var player = event.target;
				$(player).appendTo("#team1tradeoptions div");
			});

			// This handles clicking a player in "Trade Options" and puts them back
			$("#team1tradeoptions div").click(function(event) {
				var player = event.target;
				$("#teamplayers2").prepend(player);
			});
			$("#team2tradeoptions div").click(function(event) {
				var player = event.target;
				$("#teamplayers1").prepend(player);
			});

			// This is just putting the Test Trade button
			$(".container").append('<button id="testtrade" type="button" class="btn btn-primary btn-lg btn-block">Test Trade!</button>');
		}
	};
	
	// Arbitrary arrays of player names
	var team1players = ['G. Hayward', 'Al Horford', 'Kyrie Irving', 'Jayson Tatum', 'M. Morris',
					    'Greg Monroe', 'Jaylen Brown', 'Marcus Smart', 'Aron Baynes', 'G. Yabusele'];
	var team2players = ['Allen Crabbe', 'T. Mozgov', 'D. Carroll', 'Jeremy Lin', 'D. Russell',
					    'J. Okafor', 'Nik Stauskas', 'D. Cunningham', 'J. Allen', 'Quincy Acy'];

	// This handles what happens when each dropdown is clicked			
	$('#team11').click(function() {
		$('#dropdownMenuButton1').text('Team1');
		// We go through every player in Team 1, and add them in the list
		for (i = 0; i < team1players.length; i++) {
			$("#teamplayers1").append('<button id="player' + (i + 11) + '" type="button" class="list-group-item list-group-item-action">' + team1players[i] + '</button>')
		}
		readyToTrade();
	});
	// Same stuff here
	$('#team22').click(function() {
		$('#dropdownMenuButton2').text('Team2');
		for (i = 0; i < team2players.length; i++) {
			$("#teamplayers2").append('<button id="player' + (i + 21) + '" type="button" class="list-group-item list-group-item-action">' + team2players[i] + '</button>')
		}
		readyToTrade();
	});
});