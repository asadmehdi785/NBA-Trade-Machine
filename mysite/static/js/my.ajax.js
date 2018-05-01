// This file contains an assortment of functions used in the main functionality
// of the system. Most of this functionality is for the main trade page.

// Creating a function to handle formating the salaries of players correctly.
// Source: https://stackoverflow.com/questions/149055/how-can-i-format-numbers-as-dollars-currency-string-in-javascript
Number.prototype.formatMoney = function(c, d, t) {
    var n = this,
    c = isNaN(c = Math.abs(c)) ? 2 : c,
    d = d == undefined ? "." : d,
    t = t == undefined ? "," : t,
    s = n < 0 ? "-" : "",
    i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))),
    j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};

$.ajaxSetup({
    data: {
        csrfmiddlewaretoken: '{{ csrf_token }}'
    },
});

/* the trigger button to add team 3 and remove team 3*/
$('#addTeam3Btn').click(function() {
    if ($('#team3').hasClass("d-none")) {
        $('#team3').removeClass("d-none");
        $('#addTeam3Btn').html("Remove Team 3 ?")
        $('#teamplayers3').html('');
        $('#dropablelist3').html('');
    } else {
        $('#team3').addClass("d-none");
        $('#addTeam3Btn').html("Add Team 3 ?")
        $('#teamplayers3').html('');
        $('#dropablelist3').html('');
    }
});

/*on selecting the 1st team the list of players to be given*/
$('.team1dropdown').on("click", function() {
    team_id = $(this).val();
    $.ajax({
        method: "POST",
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },
        url: "/get_player_by_team",
        data: {
            "team_id": team_id
        },
        success: function(res) {
            var player_list = '';
            res = JSON.parse(res);
            res.forEach(function(data, idx) {
                var salary = data['salary']
                var ppg = data['ppg']
                var rpg = data['rpg']
                var apg = data['apg']
                player_list += '<li class="list-group-item player" data-name="' +
                    data['playerName'] + '" data-salary="' + salary + '" data-ppg="' +
                    ppg + '" data-rpg="' + rpg + '" data-apg="' + apg + '" id=' +
                    "player_" + data['id'] + ' data-team="' + data['teamName'] + '" >' +
                    data['playerName'] + '</li>';
            });
            $('#teamplayers1').html(player_list);
        },
        error: function(res) {
            console.log(res);
        }
    });
});

$(document).on("click", function() {
    var dropdown1text = $('#dropdownMenuButton1').text()
    var dropdown2text = $('#dropdownMenuButton2').text()
    var dropdown3text = $('#dropdownMenuButton3').text()
    if (dropdown1text === dropdown2text) {
        //if  any two  dropdown contains same team then no action
        $("#testtrade").removeClass('d-block');
        return;
    } else if (dropdown2text === dropdown3text) {
        //if  any two  dropdown contains same team then no action
        $("#testtrade").removeClass('d-block');
        return;
    } else if (dropdown1text === dropdown3text) {
        //if  any two  dropdown contains same team then no action
        $("#testtrade").removeClass('d-block');
        return;
    } else {
        $("#testtrade").addClass('d-block');
    }
});

// showing list of players for team 2
$('.team2dropdown').on("click", function() {
    team_id = $(this).val();
    $.ajax({
        method: "POST",
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },
        url: "/get_player_by_team",
        data: {
            "team_id": team_id
        },
        success: function(res) {
            var player_list = '';
            res = JSON.parse(res);
            res.forEach(function(data, idx) {
                var salary = data['salary']
                var ppg = data['ppg']
                var rpg = data['rpg']
                var apg = data['apg']
                player_list += '<li class="list-group-item player" data-name="' +
                    data['playerName'] + '" data-salary="' + salary + '" data-ppg="' +
                    ppg + '" data-rpg="' + rpg + '" data-apg="' + apg + '" id=' +
                    "player_" + data['id'] + ' data-team="' + data['teamName'] + '" >' +
                    data['playerName'] + '</li>';
            });
            $('#teamplayers2').html(player_list);
        },
        error: function(res) {
            console.log(res);
        }
    });
});

// showing list of players for team 3
$('.team3dropdown').on("click", function() {
    team_id = $(this).val();
    $.ajax({
        method: "POST",
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },
        url: "/get_player_by_team",
        data: {
            "team_id": team_id
        },
        success: function(res) {
            var player_list = '';
            res = JSON.parse(res);
            res.forEach(function(data, idx) {
                var salary = data['salary']
                var ppg = data['ppg']
                var rpg = data['rpg']
                var apg = data['apg']
                player_list += '<li class="list-group-item player" data-name="' +
                    data['playerName'] + '" data-salary="' + salary + '" data-ppg="' +
                    ppg + '" data-rpg="' + rpg + '" data-apg="' + apg + '" id=' +
                    "player_" + data['id'] + ' data-team="' + data['teamName'] + '" >' +
                    data['playerName'] + '</li>';
            });
            $('#teamplayers3').html(player_list);
        },
        error: function(res) {
            console.log(res);
        }
    });
});

// This handles what happens when you click test trade button
$("#testtrade").click(function() {
    var allteam1options = $("#dropablelist1").children();
    var allteam2options = $("#dropablelist2").children();
    var allteam3options = $("#dropablelist3").children();

    var currentteam1players = [];
    var currentteam2players = [];
    var currentteam3players = [];

    player = $(allteam1options[0]).text();

    for (var i = 0; i < allteam1options.length; i++) {
        currentteam1players.push($(allteam1options[i]).text());
    }
    for (var i = 0; i < allteam2options.length; i++) {
        currentteam2players.push($(allteam2options[i]).text());
    }
    for (var i = 0; i < allteam3options.length; i++) {
        currentteam3players.push($(allteam3options[i]).text());
    }

    $('#currentteam1players').val(JSON.stringify(currentteam1players));
    $('#currentteam2players').val(JSON.stringify(currentteam2players));
    $('#currentteam3players').val(JSON.stringify(currentteam3players));

    var currentteam1players = $('#currentteam1players').val();
    var currentteam2players = $('#currentteam2players').val();
    var currentteam3players = $('#currentteam3players').val();

    var dropdown1text = $('#dropdownMenuButton1').text();
    var dropdown2text = $('#dropdownMenuButton2').text();
    var dropdown3text = $('#dropdownMenuButton3').text();

    $.ajax({
        method: "POST",
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        },
        url: "/test_trade/",
        data: {
            'trade_options1': currentteam1players,
            'trade_options2': currentteam2players,
            'trade_options3': currentteam3players,
            'team1': dropdown1text,
            'team2': dropdown2text,
            'team3': dropdown3text,
        },
        success: function(res) {
            if (res.status == 0) {
                window.location.replace('/failure/');
            } else if (res.status == 1) {
                window.location.replace('/success/');
            }
        },
        error: function(res) {
            console.log(res);
        }
    });
});

/* on mouse hover show the player details if click is true*/
$(document).on("mouseover", 'li.player', function(event) {
    console.log("Mouse Hover:");
    if ($(this).attr('data-toggle') === 'tooltip') {
        return;
    }
    $(this).attr("data-toggle", "tooltip");
    $(this).attr("data-placement", "top");
    var name = $(this).attr('data-name');
    var id = $(this).attr('id');
    var salary = $(this).attr('data-salary');
    salary = Number(salary);
    salary = salary.formatMoney(2);
    salary = salary.slice(0, -3);
    var ppg = $(this).attr('data-ppg');
    var rpg = $(this).attr('data-rpg');
    var apg = $(this).attr('data-apg');
    var team = $(this).attr('data-team');
    $(this).attr("data-original-title", "<a class='btn btn-sm'>ppg: " + ppg +
        "</a><a class='btn btn-sm'>rpg: " + rpg +
        "</a><a class='btn btn-sm'>apg: " + apg +
        "</a></br><a class='btn btn-sm'>Salary: $" + salary + "</a>");
    $(this).tooltip({
        trigger: 'hover',
        html: true
    }).tooltip('show');
});

/* on mouse hover show the player details if click is true*/
$(document).on("mouseout", 'li', function(event) {
    console.log("Mouse Out:");
    $(this).attr("data-toggle", false);
    $(this).attr("data-placement", false);
    $(this).tooltip({
        trigger: 'hover',
        html: true
    }).tooltip('hide');
    $('[data-toggle="tooltip"]').tooltip({
        trigger: 'manual'
    }).tooltip('hide');
    $('[data-toggle="tooltip"]').removeAttr('data-original-title');
    $('[data-toggle="tooltip"]').removeAttr('data-toggle');
    $('[data-toggle="tooltip"]').removeAttr('data-placement');
});
