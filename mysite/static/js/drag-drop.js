$(function() {
    //Team 1===> 2 and 3
    //This function says that the TEAM1 Player List can be dropped to DropList of TEAM2 and TEAM3
    $('#teamplayers1').sortable({
        revert: true,
        connectWith: ".dropablelist2,.dropablelist3"
    }).disableSelection();
    //This function says that the TEAM2 Player List can be dropped to DropList of TEAM1 and TEAM3

    $('#teamplayers2').sortable({
        revert: true,
        connectWith: ".dropablelist1,.dropablelist3"
    }).disableSelection();
    //This function says that the TEAM3 Player List can be dropped to DropList of TEAM1 and TEAM2

    $('#teamplayers3').sortable({
            revert: true,
            connectWith: ".dropablelist1,.dropablelist2"
    }).disableSelection();

    //This function says that the Droplist of TEAM1  List can be dropped  back to to Player List of TEAM2 and TEAM3

    $('.dropablelist1').sortable({
        revert: true,
        connectWith: "#teamplayers2,#teamplayers3"
    }).disableSelection();

    //This function says that the Droplist of TEAM2  List can be dropped  back to to Player List of TEAM1 and TEAM3

    $('.dropablelist2').sortable({
        revert: true,
        connectWith: "#teamplayers1,#teamplayers3"
    }).disableSelection();

    //This function says that the Droplist of TEAM3  List can be dropped  back to to Player List of TEAM1 and TEAM2

    $('.dropablelist3').sortable({
        revert: true,
        connectWith: "#teamplayers1,#teamplayers2"
    }).disableSelection();

});



