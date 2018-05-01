# This is the main view handler for our system. Requests are routed from the
# 'urls.py' file and matched up with a view in this file. Then, once a view is
# matched, that particular function is run, usually ending in a render() call
# in most cases.

# These modules are needed for many of the functions we have defined
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import Team, Player, Transaction, History

import json
import uuid
import datetime

# This handles a request to our index page. The 'index.html' template is
# rendered after a call to this. More information on 'index.html' can be found
# in the 'templates' directory.
def home(request):
    return render(request, 'index.html')

# This handles a request to our login/signup page. If the user logs in correctly,
# then they are redirected to the main trade page. A request to the signup page
# brings them to 'signup.html'
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('trade')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# This handles a request to our "About Us" page.
def about_us(request):
    return render(request, 'about_us.html')

# This handles a request to our "Privacy" page.
def privacy(request):
    return render(request, 'privacy.html')

# This handles a request to our "Terms" page.
def terms(request):
    return render(request, 'terms.html')

# This handles a request to our "Rules" page.
def rules(request):
    return render(request, 'rules.html')

# This handles a request to our trade view. We first initialize our Team and
# Player models so that they can be used within the 'trade.html' template.
# We then pass them in via the render() function.
def trade(request):
    teams = Team.objects.all()
    players = Player.objects.all()
    return render(request, 'trade.html', {'teams': teams, 'players': players})

# This is the main function to test a trade. Essentially, when the "Try Trade"
# button is clicked, this is the view that gets requested. Currently, whether
# a trade is valid or not is determined through checking the salary caps of the
# respective teams conducting a trade. The salaries of the individual players
# are also taken into account. These follow the rules set in the Collective
# Bargaining Agreement (CBA).
# @csrf_exempt to disable csrf for this function.
@csrf_exempt
def test_trade(request):
    # Getting our list of trade options for each team
    trade_options1=request.POST.get('trade_options1')
    trade_options2=request.POST.get('trade_options2')

    # Converting the trade options to a more easily parseable JSON format
    trade_options1=json.loads(trade_options1)
    trade_options2=json.loads(trade_options2)

    # Remove team1, team2, team3 from session
    # See Django documentation for more details on how sessions work:
    # https://docs.djangoproject.com/en/1.11/topics/http/sessions/
    if 'team1' in request.session:
        del request.session['team1']
    if 'team2' in request.session:
        del request.session['team2']
    if 'team3' in request.session:
        del request.session['team3']
    if 'list1' in request.session:
        del request.session['list1']
    if 'list2' in request.session:
        del request.session['list2']
    if 'list3' in request.session:
        del request.session['list3']

    # Remove other data from session
    if 'team1payRoll_beforeTrade' in request.session:
        del request.session['team1payRoll_beforeTrade']
    if 'team2payRoll_beforeTrade' in request.session:
        del request.session['team2payRoll_beforeTrade']
    if 'team3payRoll_beforeTrade' in request.session:
        del request.session['team3payRoll_beforeTrade']
    if 'team1payRoll_afterTrade' in request.session:
        del request.session['team1payRoll_afterTrade']
    if 'team2payRoll_afterTrade' in request.session:
        del request.session['team2payRoll_afterTrade']
    if 'team3payRoll_afterTrade' in request.session:
        del request.session['team3payRoll_afterTrade']

    # Checking to make sure if trade_options for each team is actually defined.
    # We then add some session data if this is true.
    if len(trade_options1) > 0:
        p = trade_options1[0]
        player = Player.objects.filter(playerName=p).first()
        team2 = player.playerTeam
        request.session['team2'] = team2.teamName
    if len(trade_options2)>0:
        p = trade_options2[0]
        player = Player.objects.filter(playerName=p).first()
        team1 = player.playerTeam
        request.session['team1'] = team1.teamName

    # Calculating salary for each set of trade options
    team1_sum_salary = 0
    for p in trade_options2:
        player = Player.objects.filter(playerName=p).first()
        player_salary = player.playerSalary
        team1_sum_salary += player_salary
    team2_sum_salary = 0
    for p in trade_options1:
        player = Player.objects.filter(playerName=p).first()
        player_salary = player.playerSalary
        team2_sum_salary += player_salary

    # Accessing the payrolls for each team
    team1_payRoll = team1.teamPayroll
    team2_payRoll = team2.teamPayroll

    # Storing teams' payrolls in session
    request.session['team1payRoll_beforeTrade'] = team1_payRoll
    request.session['team2payRoll_beforeTrade'] = team2_payRoll

    # Subtracting salaries of playing going away from team and then adding
    # salaries of players coming to teams
    team1_payRoll -= team1_sum_salary
    team2_payRoll -= team2_sum_salary
    team1_payRoll += team2_sum_salary
    team2_payRoll += team1_sum_salary
    
    # Now we have to check if each team is over the salary cap or not. Initially,
    # we assume that both teams are below the cap.
    team1_overcap = False
    team2_overcap = False

    # Adding more information to session
    request.session['team1payRoll_afterTrade'] = team1_payRoll
    request.session['team2payRoll_afterTrade'] = team2_payRoll
    request.session['cap'] = 99093000

    # Checking if any team is over cap
    if team1_payRoll > 99093000:
        team1_overcap = True
    if team2_payRoll > 99093000:
        team1_overcap = True

    # Additional handling for when a third team is involved in the trade.
    if 'trade_options3' in request.POST:
        trade_options3 = request.POST.get('trade_options3')
        trade_options3 = json.loads(trade_options3)
        if len(trade_options3) > 0:
            p = trade_options3[0]
            player = Player.objects.filter(playerName=p).first()
            team3 = player.playerTeam
            request.session['team3'] = team3.teamName

            team3_sum_salary = 0
            for p in trade_options3:
                player = Player.objects.filter(playerName=p).first()
                player_salary = player.playerSalary
                team2_sum_salary += player_salary

            team3_payRoll = team3.teamPayroll
            request.session['team3payRoll_beforeTrade'] = team3_payRoll
            team3_payRoll += team2_sum_salary
            request.session['team3payRoll_afterTrade'] = team3_payRoll
            if team3_payRoll > 99093000:
                team3_overcap = True
            if team3_overcap:
                if team3_sum_salary > 1.25 * team2_sum_salary:
                    response = {'status': 0}
                else:
                    response = {'status': 1}

    # Doing some other checks
    if team1_overcap:
        if team1_sum_salary > 1.25 * team2_sum_salary:
            response = {'status': 0}
        else:
            response = {'status': 1}
    if team2_overcap:
        if team2_sum_salary > 1.25 * team2_sum_salary:
            response = {'status': 0}
        else:
            response = {'status': 1}

    # Setting all the trading list IDs just dummy IDs
    if 'trade_history' in request.session:
        trade_history=request.session['trade_history']
        trade_history=json.loads(trade_history)
        trade_history.append(str(uuid.uuid4()))
        request.session['trade_history'] = json.dumps(trade_history)
    else:
        trade_history=list()
        trade_history.append(str(uuid.uuid4()))
        request.session['trade_history']=json.dumps(trade_history)

    # Save the list of players in the session
    request.session['list1']=json.dumps(trade_options1)
    request.session['list2'] = json.dumps(trade_options2)

    if 'trade_options3' in request.POST:
        request.session['list3'] = json.dumps(trade_options3)

    return HttpResponse(json.dumps(response), content_type='application/json')

# If the test fails, then the system will be routed to this view.
# Essentially, we are passing in the data that is defined in the session to the
# 'failure.html' template, so that relevant data can be displayed there.
def failure(request):
    # Getting all our data from session
    team1 = request.session['team1']
    team2 = request.session['team2']
    if 'team3' in request.session:
        team3 = request.session['team3']

    # Getting the payrolls before the trade from the session
    team1payRoll_beforeTrade = request.session['team1payRoll_beforeTrade']
    team2payRoll_beforeTrade = request.session['team2payRoll_beforeTrade']
    if 'team3payRoll_beforeTrade' in request.session:
        team3payRoll_beforeTrade = request.session['team3payRoll_beforeTrade']

    # Getting the payrolls after the trade from the session
    team1payRoll_afterTrade = request.session['team1payRoll_afterTrade']
    team2payRoll_afterTrade = request.session['team2payRoll_afterTrade']
    if 'team3payRoll_afterTrade' in request.session:
        team3payRoll_afterTrade = request.session['team3payRoll_afterTrade']

    # Additional data that may or may not be passed in
    if 'trade_history' in request.session:
        trade_history=request.session['trade_history']
        trade_history=json.loads(trade_history)
        trade_history=trade_history[-1]
    if 'list1' in request.session:
        list1=json.loads(request.session['list1'])
        print(list1)
    if 'list2' in request.session:
        list2 = json.loads(request.session['list2'])
        print(list2)
    if 'list3' in request.session:
        list3 = json.loads(request.session['list3'])
        print(list3)

		
	if request.user.is_authenticated:	
		# Store result in database
		# Transaction table
		transaction = Transaction()
		transaction.date = datetime.datetime.now()
		if 'trade_history' in locals():
			transaction.tradeId = trade_history
		userid = request.user.id
		username = request.user.username
		transaction.team1Name = team1
		transaction.team2Name = team2

		if 'team3' in locals():
			transaction.team3Name = team3

		transaction.userId = request.user
		transaction.result = 'Failure'

		transaction.team1PayrollBefore = team1payRoll_beforeTrade
		transaction.team2PayrollBefore = team2payRoll_beforeTrade
		if 'team3payRoll_beforeTrade' in locals():
			transaction.team3PayrollBefore = team3payRoll_beforeTrade

		transaction.team1PayrollAfter = team1payRoll_afterTrade
		transaction.team2PayrollAfter = team2payRoll_afterTrade
		if 'team3payRoll_afterTrade' in locals():
			transaction.team3PayrollAfter = team3payRoll_afterTrade

		# Save only when the user in logged in
		if(request.user.is_authenticated):
			transaction.save()

		# History
		if 'list1' in locals() and request.user.is_authenticated:
			for plyer in list1:
				history = History()
				history.playerName = plyer
				history.tradeId =transaction
				history.team = 'Team1'
				history.save()
		if 'list2' in locals() and request.user.is_authenticated:
			for plyer in list2:
				history = History()
				history.playerName = plyer
				history.tradeId = transaction
				history.team = 'Team2'
				history.save()
		if 'list3' in locals() and request.user.is_authenticated:
			for plyer in list3:
				history = History()
				history.playerName = plyer
				history.tradeId = transaction
				history.team = 'Team3'
				history.save()

    return render(request, 'failure.html', locals())

# If a trade succeeds then the system will route to this view. This is very
# similar to the 'failure' view, except that 'success.html' will be the template
# that the data will be passed into.
def success(request):
    # Getting all our data from session
    team1 = request.session['team1']
    team2 = request.session['team2']
    if 'team3' in request.session:
        team3 = request.session['team3']

    # Getting the payrolls before the trade from the session
    team1payRoll_beforeTrade = request.session['team1payRoll_beforeTrade']
    team2payRoll_beforeTrade = request.session['team2payRoll_beforeTrade']
    if 'team3payRoll_beforeTrade' in request.session:
        team3payRoll_beforeTrade = request.session['team3payRoll_beforeTrade']

    # Getting the payrolls after the trade from the session
    team1payRoll_afterTrade = request.session['team1payRoll_afterTrade']
    team2payRoll_afterTrade = request.session['team2payRoll_afterTrade']
    if 'team3payRoll_afterTrade' in request.session:
        team3payRoll_afterTrade = request.session['team3payRoll_afterTrade']

    # Additional data that may or may not be passed in
    if 'trade_history' in request.session:
        trade_history=request.session['trade_history']
        trade_history=json.loads(trade_history)
        trade_history=trade_history[-1];
    if 'list1' in request.session:
        list1=json.loads(request.session['list1'])
        print(list1)
    if 'list2' in request.session:
        list2 = json.loads(request.session['list2'])
        print(list2)
    if 'list3' in request.session:
        list3 = json.loads(request.session['list3'])
        print(list3)
	
	if request.user.is_authenticated:
		# Store result in database
		# Transaction table
		transaction = Transaction()
		transaction.date = datetime.datetime.now()
		if 'trade_history' in locals():
			transaction.tradeId = trade_history
		userid = request.user.id
		username = request.user.username
		transaction.team1Name = team1
		transaction.team2Name = team2

		if 'team3' in locals():
			transaction.team3Name = team3

		transaction.userId = request.user
		transaction.result = 'Success'

		transaction.team1PayrollBefore = team1payRoll_beforeTrade
		transaction.team2PayrollBefore = team2payRoll_beforeTrade
		if 'team3payRoll_beforeTrade' in locals():
			transaction.team3PayrollBefore = team3payRoll_beforeTrade

		transaction.team1PayrollAfter = team1payRoll_afterTrade
		transaction.team2PayrollAfter = team2payRoll_afterTrade
		if 'team3payRoll_afterTrade' in locals():
			transaction.team3PayrollAfter = team3payRoll_afterTrade

		# Save only when the user in logged in
		if(request.user.is_authenticated):
			transaction.save()

		# History
		if 'list1' in locals() and request.user.is_authenticated:
			for plyer in list1:
				history = History()
				history.playerName = plyer
				history.tradeId =transaction
				history.team = 'Team1'
				history.save()
		if 'list2' in locals() and request.user.is_authenticated:
			for plyer in list2:
				history = History()
				history.playerName = plyer
				history.tradeId = transaction
				history.team = 'Team2'
				history.save()
		if 'list3' in locals() and request.user.is_authenticated:
			for plyer in list3:
				history = History()
				history.playerName = plyer
				history.tradeId = transaction
				history.team = 'Team3'
				history.save()

    return render(request,'success.html',locals())

# This view will return the list of players within the selected team as a JSON
# array.
# This will usually be called through AJAX from the 'my.ajax.js' file.
@csrf_exempt
def get_player_by_team(request):
    # Get Team ID that was selected
    team_id=request.POST.get("team_id")
    
    # To get the actual team name
    teams=Team.objects.all().filter(id=team_id)
    for team in teams:
        team_name=team.teamName

    # Get all players in a team
    players=Player.objects.all().filter(playerTeam_id=team_id)
    # Prepare a JSON array
    json_resp=[]
    for player in players :
        obj={}
        obj['id']=player.id
        obj['playerName']=player.playerName
        obj['playerTeam_id']=player.playerTeam_id
        obj['teamName']=team_name
        obj['salary'] = player.playerSalary
        obj['ppg'] = player.playerppg
        obj['rpg'] = player.playerrpg
        obj['apg'] = player.playerapg
        json_resp.append(obj)
    resp = json.dumps(json_resp)

    # Send JSON response to the AJAX call
    return HttpResponse(resp)


# This function will return the details of a particuar player
def get_player_info(request):
    player_id=request.POST.get("player_id")
    players=Player.objects.filter(id=player_id).first()
    json_resp = []
    for player in players:
        obj = {}
        obj['id'] = player.id
        obj['playerName'] = player.playerName
        obj['playerTeam_id'] = player.playerTeam_id
        json_resp.append(obj)
    resp = json.dumps(json_resp)

    # Send JSON response to the AJAX call
    return HttpResponse(resp)

# Trade history page:
# Listing the trade done by a user.
def trade_history(request):
    if request.user.is_authenticated:
        trade_history_data=Transaction.objects.filter(userId=request.user).all()
    return render(request, 'trade_history.html',locals())

# Trade result page:
# Show the details of a trade transaction
def trade_result(request):
    # Get the trade ID from GET request
    tradeId=request.GET.get('id')

    # Get the transaction details of the trade ID
    trade_transaction=Transaction.objects.filter(tradeId=tradeId).first()

    # Team list 1
    teamlist1=History.objects.filter(tradeId=trade_transaction).filter(team='Team1').all()
    list1=[]
    for t1 in teamlist1:
        list1.append(t1.playerName)

    # Team list 2
    teamlist2 = History.objects.filter(tradeId=trade_transaction).filter(team='Team2').all()
    list2 = []
    for t2 in teamlist2:
        list2.append(t2.playerName)

    # Team list3
    teamlist3 = History.objects.filter(tradeId=trade_transaction).filter(team='Team3').all()
    list3 = []
    for t3 in teamlist3:
        list3.append(t3.playerName)

    # Result of trade transaction
    result = trade_transaction.result

    # Team name involved in trade transaction
    team1 = trade_transaction.team1Name
    team2 = trade_transaction.team2Name
    team3 = trade_transaction.team3Name

    # Team payroll details
    team1payRoll_beforeTrade = trade_transaction.team1PayrollBefore
    team2payRoll_beforeTrade = trade_transaction.team2PayrollBefore
    team3payRoll_beforeTrade = trade_transaction.team3PayrollBefore

    team1payRoll_afterTrade = trade_transaction.team1PayrollAfter
    team2payRoll_afterTrade = trade_transaction.team2PayrollAfter
    team3payRoll_afterTrade = trade_transaction.team3PayrollAfter

    # Returning all the details to the trade_result page
    return render(request,'trade_result.html',locals())