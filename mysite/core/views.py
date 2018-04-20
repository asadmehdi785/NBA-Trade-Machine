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

# Importing our Team and Player models
from .models import Team, Player

import json
import uuid

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
@csrf_exempt
def test_trade(request):
    
    # Getting our list of trade options for each team
    trade_options1=request.POST.get('trade_options1')
    trade_options2=request.POST.get('trade_options2')

    # Converting the trade options to a more easily parseable JSON format
    trade_options1=json.loads(trade_options1)
    trade_options2=json.loads(trade_options2)

    # Clearing current session data. This is needed to be done before a trade is
    # tested, because the system uses sessions in order to use data between
    # different views.
    # See Django documentation for more details:
    # https://docs.djangoproject.com/en/1.11/topics/http/sessions/
    request.session.clear()

    # Checking to make sure if trade_options for each team is actually defined.
    # We then add some session data if this is true.
    if len(trade_options1)>0:
        p = trade_options1[0]
        player = Player.objects.filter(playerName=p).first()
        team2 = player.playerTeam
        request.session['team2'] = team2.teamName
    if len(trade_options2)>0:
        p = trade_options2[0]
        player = Player.objects.filter(playerName=p).first()
        team1 = player.playerTeam
        request.session['team1'] = team1.teamName

    # Calculating total salary for the trade options for each team
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
    # As of the beta release, this code is not fully fleshed out, and needs to
    # be improved further. However, trades between two teams works as expected.
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

    # If none of the teams are over the cap then the trade is automatically
    # successful
    if not team1_overcap and not team2_overcap and not team3_overcap:
        response = {'status': 1}
        return HttpResponse(json.dumps(response), content_type='application/json')

    # If a team is over the cap, then we check if the sum of their salary is
    # 1.25 times the sum of the other team's salary. If this is the case, then
    # the trade fails (we return a 'status' of 0 back to the AJAX handler in the
    # the front-end).
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

    # Setting the unique trade ID in the session
    if 'trade_history' in request.session:
        trade_history=request.session['trade_history']
        trade_history=json.loads(trade_history)
        trade_history.append(str(uuid.uuid4()))
        request.session['trade_history'] = json.dumps(trade_history)
    else:
        trade_history=list()
        trade_history.append(str(uuid.uuid4()))
        request.session['trade_history']=json.dumps(trade_history)

    # Saving the list of players in the session
    request.session['list1']=json.dumps(trade_options1)
    request.session['list2'] = json.dumps(trade_options2)

    # Additional handling for the team 3 options
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
    if 'list2' in request.session:
        list2 = json.loads(request.session['list2'])
    if 'list3' in request.session:
        list3 = json.loads(request.session['list3'])

    '''
    return render(request, 'failure.html', {'team1': team1, 'team2': team2, 'team1payRoll_beforeTrade': team1payRoll_beforeTrade,\
                                            'team2payRoll_beforeTrade': team2payRoll_beforeTrade, 'team1payRoll_afterTrade': team1payRoll_afterTrade,\
                                            'team2payRoll_afterTrade': team2payRoll_afterTrade})
    '''
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
    ''' 
    return render(request, 'success.html', {'team1': team1, 'team2': team2, 'team1payRoll_beforeTrade': team1payRoll_beforeTrade,\
                                            'team2payRoll_beforeTrade': team2payRoll_beforeTrade, 'team1payRoll_afterTrade': team1payRoll_afterTrade,\
                                            'team2payRoll_afterTrade': team2payRoll_afterTrade})
    '''

    return render(request,'success.html',locals())

# @csrf_exempt to disable csrf for this function.
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
    resp =json.dumps(json_resp)

    # Send JSON response to the AJAX call
    return HttpResponse(resp)

# This function will return the details of a particuar player
@csrf_exempt
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

# @csrf_exempt
# def get_player_stuff_test(request):
#     player_list=request.POST.getlist('player_list[]')
#     json_resp = []
#     print ("player_list:"+str(player_list))
#     print ("type(player_list):"+str(type(player_list)))
#     for p in player_list:
#         print ("p: "+str(p))
#         player = Player.objects.get(playerName=p)
#         obj = {}
#         obj['id'] = player.id
#         obj['playerName'] = player.playerName
#         json_resp.append(obj)

#     # players=Player.objects.filter(id=player_id).first()
#     # json_resp = []
#     # for player in players:
#     #     obj = {}
#     #     obj['id'] = player.id
#     #     obj['playerName'] = player.playerName
#     #     obj['playerTeam_id'] = player.playerTeam_id
#     #     json_resp.append(obj)
#     resp = json.dumps(json_resp)
#     print(resp)
#     return HttpResponse(resp) #send json response to ajax call