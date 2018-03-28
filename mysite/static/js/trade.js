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

			// We bring the "Trade Options" part up here
			var team1Div = $('#team1');
			$("#team1tradeoptions").toggleClass('d-none d-block');
			var team2Div = $('#team2');
			$("#team2tradeoptions").toggleClass('d-none d-block');
			var team3Div = $('#team3');
			$("#team3tradeoptions").toggleClass('d-none d-block');


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
			$("#teamplayers2").click(function(event) {
				var player = event.target;
				$(player).appendTo("#team1tradeoptions div");

				var allteam1options = $("#team1tradeoptions div").children();
				var allteam2options = $("#team2tradeoptions div").children();

				if (allteam1options.length === 1 && allteam2options.length === 1) {
					team1options_playername = $(allteam1options[0]).text();
					team2options_playername = $(allteam2options[0]).text();

					if (team1options_playername === "Daniel Theis" && team2options_playername === "Kent Bazemore") {
						$("#testtradeNotSuccessful").toggleClass('d-none d-block');
						$("#testtrade").toggleClass('d-block d-none');
					}
				}
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
			$("#testtrade").toggleClass('d-none d-block');
		}
	};
	
	// Arbitrary arrays of player names
	var team1players = ['Kent Bazemore', "DeAndre' Bembry", 'Tyler Cavanaugh', 'Antonius Cleveland', 'John Collins',
					    'Dewayne Dedmon', 'Malcolm Delaney', 'Tyler Dorsey', 'Damion Lee', 'Josh Magette',
					    'Jaylen Morris', 'Mike Muscala', 'Miles Plumlee', 'Taurean Prince', 'Dennis Schroder',
					    'Isaiah Taylor', 'Andrew White III'];
	var team2players = ['Kyrie Irving', 'Jaylen Brown', 'Jayson Tatum', 'Jayson Tatum', 'Marcus Morris',
					    'Al Horford', 'Terry Rozier', 'Marcus Smart', 'Greg Monroe', 'Aron Baynes',
					    'Daniel Theis', 'Shane Larkin', 'Abdel Nader', 'Semi Ojeleye', 'Gordon Hayward',
					    'Guerschon Yabusele', 'Jabari Bird'];
	var team3players = ['Quincy Acy', 'Jarrett Allen', 'DeMarre Carroll', 'Allen Crabbe','Dante Cunningham',
						'Spencer Dinwiddie', 'Milton Doyle', 'Joe Harris', 'Rondae Hollis-Jefferson', 'Caris LeVert',
						'Jeremy Lin', 'Timofey Mozgov', 'Jahlil Okafor', "D'Angelo Russell", 'Nik Stauskas',
						'James Webb III', '	Isaiah Whitehead'];

	// This handles what happens when each dropdown is clicked			
	$('#team11').click(function() {
		$('#dropdownMenuButton1').text('Atlanta Hawks');
		// We go through every player in Team 1, and add them in the list
		for (i = 0; i < team1players.length; i++) {
			$("#teamplayers1").append('<button id="player' + (i + 11) + '" type="button" class="list-group-item list-group-item-action">' + team1players[i] + '</button>')
		}
		readyToTrade();
	});
	// Same stuff here
	$('#team22').click(function() {
		$('#dropdownMenuButton2').text('Boston Celtics');
		for (i = 0; i < team2players.length; i++) {
			$("#teamplayers2").append('<button id="player' + (i + 21) + '" type="button" class="list-group-item list-group-item-action">' + team2players[i] + '</button>')
		}
		readyToTrade();
	});
	$('#team33').click(function() {
		$('#dropdownMenuButton3').text('Brooklyn Nets');
		for (i = 0; i < team3players.length; i++) {
			$("#teamplayers3").append('<button id="player' + (i + 31) + '" type="button" class="list-group-item list-group-item-action">' + team3players[i] + '</button>')
		}
		readyToTrade();
	});

	$('#addteam3').click(function() {
		$("#team3").toggleClass('d-none d-block');
		$("#addteam3").toggleClass('d-block d-none');
	});
});