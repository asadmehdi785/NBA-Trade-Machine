
/* the trigger button to add team 3 and remove team 3*/
$('#addTeam3Btn').click(function () {
    if($('#team3').hasClass("d-none")){
        $('#team3').removeClass("d-none");
        $('#addTeam3Btn').html("Remove Team 3 ?")
    }else{
        $('#team3').addClass("d-none");
        $('#addTeam3Btn').html("Add Team 3 ?")
    }

});

/*on selecting the 1st team the list of players to be given*/

$('.team1dropdown').on("click",function(){
    team_id=$(this).val();
    $.ajax({
          method: "POST",
          url: "/get_player_by_team",
          data:{
              "team_id":team_id
          },
        success:function (res) {
            var player_list='';
            res=JSON.parse(res);
                res.forEach(function (data,idx) {
                    var salary = data['salary']
                    var ppg = data['ppg']
                    var rpg = data['rpg']
                    var apg = data['apg']

                    player_list+='<li class="list-group-item player" data-name="'+data['playerName']+
                    '" data-salary="' + salary + '" data-ppg="'+ppg+ '" data-rpg="' + rpg + '" data-apg="' + apg + '" id='+"player_"+data['id']+' data-team="'+data['teamName']+
                    '" >' +  data['playerName'] + '</li>';
                });
            //$('#teamplayers1').append(player_list);
            $('#teamplayers1').html(player_list);
        },error:function (res) {
                console.log(res);
        }
    });

});

$(document).on("click",function(){
        var dropdown1text = $('#dropdownMenuButton1').text()
		var dropdown2text = $('#dropdownMenuButton2').text()
		var dropdown3text = $('#dropdownMenuButton3').text()

			if(dropdown1text===dropdown2text){
				//if  any two  dropdown contains same team then no action
	            $("#testtrade").removeClass('d-block');
				return ;
			}else if(dropdown2text===dropdown3text){
				//if  any two  dropdown contains same team then no action
                $("#testtrade").removeClass('d-block');
				return ;
			}else if(dropdown1text===dropdown3text){
				//if  any two  dropdown contains same team then no action
                $("#testtrade").removeClass('d-block');
				return ;
			}else{
                        $("#testtrade").addClass('d-block');

            }



});


// showing list of players for team 2
$('.team2dropdown').on("click",function(){
    team_id=$(this).val();
    $.ajax({
          method: "POST",
          url: "/get_player_by_team",
          data:{
              "team_id":team_id
          },
        success:function (res) {
            var player_list='';
            res=JSON.parse(res);
                res.forEach(function (data,idx) {
                    var salary = data['salary']
                    var ppg = data['ppg']
                    var rpg = data['rpg']
                    var apg = data['apg']

                    player_list+='<li class="list-group-item player" data-name="'+data['playerName']+
                    '" data-salary="' + salary + '" data-ppg="'+ppg+ '" data-rpg="' + rpg + '" data-apg="' + apg + '" id='+"player_"+data['id']+' data-team="'+data['teamName']+
                    '" >' +  data['playerName'] + '</li>';
                });
            //$('#teamplayers2').append(player_list);
            $('#teamplayers2').html(player_list);
        },error:function (res) {
                console.log(res);
        }
    });

});



// When you choose a player
$("#teamplayers1").click(function(event) {
    var player = event.target;
    console.log('player: ' + player);
    $(player).appendTo("#team2tradeoptions div");

    var allteam1options = $("#team1tradeoptions div").children();
    var allteam2options = $("#team2tradeoptions div").children();

    var currentteam1players = [];
    var currentteam2players = [];


    player = $(allteam2options[0]).text();

    for(var i = 0; i < allteam1options.length; i++) {
        currentteam1players.push($(allteam1options[i]).text());
    }
    for(var i = 0; i < allteam2options.length; i++) {
        currentteam2players.push($(allteam2options[i]).text());
    }



    $('#currentteam1players').val(JSON.stringify(currentteam1players));

    $('#currentteam2players').val(JSON.stringify(currentteam2players));
    console.log("currentteam1players:");
    console.log(currentteam1players);
    console.log("currentteam2players:");
    console.log(currentteam2players);


});



// this is the source of the bug where you have to pick a player from team 2 first
// i can probably fix this later
$("#teamplayers2").click(function(event) {
    var player = event.target;
    console.log('player: ' + player);
    $(player).appendTo("#team1tradeoptions div")

    var allteam1options = $("#team1tradeoptions div").children();
    var allteam2options = $("#team2tradeoptions div").children();

    var currentteam1players = [];
    var currentteam2players = [];

    player = $(allteam1options[0]).text();

    for(var i = 0; i < allteam1options.length; i++) {
        currentteam1players.push($(allteam1options[i]).text());
    }
    for(var i = 0; i < allteam2options.length; i++) {
        currentteam2players.push($(allteam2options[i]).text());
    }


    $('#currentteam1players').val(JSON.stringify(currentteam1players));

    $('#currentteam2players').val(JSON.stringify(currentteam2players));
    console.log("currentteam1players:");
    console.log(currentteam1players);
    console.log("currentteam2players:");
    console.log(currentteam2players);


});

// This handles what happens when you click test trade button
$("#testtrade").click(function() {
    var currentteam1players=$('#currentteam1players').val();
    var currentteam2players=$('#currentteam2players').val();
    $.ajax({
        method: "POST",
        url: "/test_trade/",
        data: {
            'trade_options1': currentteam1players,
            'trade_options2': currentteam2players
        },
        success:function(res) {
            if (res.status == 0) {
                window.location.href = '../failure'
            } else if (res.status == 1) {
                window.location.href = '../success'
            }
        }, error:function(res) {
            console.log(res);
        }
    });
});









/*on selecting the 2nd team the list of players to be given*/
// $('.team2dropdown').on("click",function(){
// console.log($(this));
//     team_id=$(this).val();
//     $.ajax({
//           method: "POST",
//           url: "/get_player_by_team",
//           data:{
//               "team_id":team_id
//           },
//         success:function (res) {
//                 console.log(res);
//             res=JSON.parse(res);
//             var player_list='';
//                 res.forEach(function (data,idx) {
//                     var price=Math.random();
//                     price=price*10;
//                     price=price.toFixed(1);

//                     player_list+='<li class="list-group-item player" data-name="'+data['playerName']+'" data-price="'+price+'" id='+"player_"+data['id']+' data-team="'+data['teamName']+'" >'+data['playerName']+'<a class="price">$'+price+'</a></li>';
//                 });
//             $('#player_list2').html(player_list);
//         },error:function (res) {
//                 console.log(res);
//         }
//     })

// });

/*on selecting the 3rd team the list of players to be given*/
// $('.team3dropdown').on("click",function(){
// console.log($(this));
//     team_id=$(this).val();
//     $.ajax({
//           method: "POST",
//           url: "/get_player_by_team",
//           data:{
//               "team_id":team_id
//           },
//         success:function (res) {
//                 console.log(res);
//             res=JSON.parse(res);
//             var player_list='';
//                 res.forEach(function (data,idx) {
//                     var price=Math.random();
//                     price=price*10;
//                     price=price.toFixed(1);

//                     player_list+='<li class="list-group-item player" data-name="'+data['playerName']+'" data-price="'+price+'" id='+"player_"+data['id']+' data-team="'+data['teamName']+'" >'+data['playerName']+'<a class="price">$'+price+'</a></li>';
//                 });
//             $('#player_list3').html(player_list);
//         },error:function (res) {
//                 console.log(res);
//         }
//     })

// });


/* move the selected player to the specific team*/
// function move(id){
//     console.log("Move---->");
//     var player_id = $(id).attr('data-id');
//     var team=$(id).attr('data-team');
//     console.log(player_id);
//     console.log(team);
//     var player=$('#'+player_id);
// 	$(player).appendTo("#teamplayers"+team);
// 	$('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('hide');
//     $('[data-toggle="tooltip"]').removeAttr('data-original-title');
//     $('[data-toggle="tooltip"]').removeAttr('data-toggle');
//     $('[data-toggle="tooltip"]').removeAttr('data-placement');

// }
/*

$("#player_list2").click(function(event) {
			 	var player = event.target;
			 	$(player).appendTo("#teamplayers1")
 });
$("#player_list3").click(function(event) {
			 	var player = event.target;
			 	$(player).appendTo("#teamplayers3")
 });
*/

/* to show the option to the user to which team the player will go*/
// $(document).on("click",'li.player',function(event){
//                 $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('hide');
//                 $(this).attr("data-toggle","tooltip");
// 	        	$(this).attr("data-placement","auto");
// 	        	console.log(event.target.id);
// 	        	console.log($(this).attr('id'));
// 	        	if($('#addTeam3Btn').html().indexOf("Remove")>=0){
// 	        	    $(this).attr("data-original-title","<button class='list-group-item' onclick='move(this);' data-team='1' data-id='"+$(this).attr('id')+"'> Team 1</button><button class='list-group-item' onclick='move(this);' data-team='2' data-id='"+$(this).attr('id')+"'> Team 2</button><button class='list-group-item' onclick='move(this);' data-team='3' data-id='"+$(this).attr('id')+"'>Team 3</button>");

//                 }else{

// 	        	    $(this).attr("data-original-title","<button class='list-group-item' onclick='move(this);' data-team='1' data-id='"+$(this).attr('id')+"'> Team 1</button><button class='list-group-item' onclick='move(this);' data-team='2' data-id='"+$(this).attr('id')+"'> Team 2</button>");

//                 }
// 	        	$(this).tooltip({trigger: 'manual',html:true}).tooltip('show');

// });

/* to remove the option of team selection popup*/

// $(':not(li.player)').on("click",function(){
//                 $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('hide');
//                 $('[data-toggle="tooltip"]').removeAttr('data-original-title');
//                 $('[data-toggle="tooltip"]').removeAttr('data-toggle');
//                 $('[data-toggle="tooltip"]').removeAttr('data-placement');




// });

Number.prototype.formatMoney = function(c, d, t){
    var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c, 
    d = d == undefined ? "." : d, 
    t = t == undefined ? "," : t, 
    s = n < 0 ? "-" : "", 
    i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))), 
    j = (j = i.length) > 3 ? j % 3 : 0;
   return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };

/* on mouse hover show the player details if click is true*/
$(document).on("mouseover",'li.player',function(event){
    console.log("Mouse Hover:");

    if($(this).attr('data-toggle')==='tooltip'){
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

    //salary = salary.formatMoney(2);
    //salary.toFixed().replace(/(\d)(?=(\d{3})+(,|$))/g, '$1,')
    console.log("salary: " + salary);
    var ppg = $(this).attr('data-ppg');
    var rpg = $(this).attr('data-rpg');
    var apg = $(this).attr('data-apg');
    var team = $(this).attr('data-team');
    $(this).attr("data-original-title", "<a class='btn btn-sm'>ppg: " + ppg + "</a><a class='btn btn-sm'>rpg: " +
                 rpg + "</a><a class='btn btn-sm'>apg: " + apg +"</a></br><a class='btn btn-sm'>Salary: $" + salary + "</a>");

    $(this).tooltip({trigger: 'hover', html: true}).tooltip('show');


});

/* on mouse hover show the player details if click is true*/
$(document).on("mouseout",'li',function(event){

    console.log("Mouse Out:");
    $(this).attr("data-toggle", false);
    $(this).attr("data-placement", false);
    $(this).tooltip({trigger: 'hover', html: true}).tooltip('hide');
    $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('hide');
    $('[data-toggle="tooltip"]').removeAttr('data-original-title');
    $('[data-toggle="tooltip"]').removeAttr('data-toggle');
    $('[data-toggle="tooltip"]').removeAttr('data-placement');



});
