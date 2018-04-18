from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import Team, Player

import json
import uuid

def home(request):
    return render(request, 'index.html')

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

def trade(request):
    teams = Team.objects.all()
    players = Player.objects.all()
    return render(request, 'trade.html', {'teams': teams, 'players': players})

# Main function to test trade
@csrf_exempt
def test_trade(request):

    print("Trade Test:")
    # Getting our list of trade options for each team
    trade_options1=request.POST.get('trade_options1')
    trade_options2=request.POST.get('trade_options2')
    print(trade_options1)
    print(trade_options2)
    trade_options1=json.loads(trade_options1)
    trade_options2=json.loads(trade_options2)

    # Clearing session
    request.session.clear()

    # I don't know if these if statements are needed
    # Basically I'm checking if the list is empty or not
    # They're probably not needed but the request.session
    # stuff is important so just keep it for now
    if len(trade_options1)>0:
        print ("here trade options 1")
        p = trade_options1[0]
        print("First Player:"+str(p))
        player = Player.objects.filter(playerName=p).first()
        team2 = player.playerTeam
        request.session['team2'] = team2.teamName

    if len(trade_options2)>0:

        print ("here trade options 2")
        p = trade_options2[0]
        print("First Player:" + str(p))

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

    team1_payRoll = team1.teamPayroll
    team2_payRoll = team2.teamPayroll

    # Storing teams' payrolls in session
    request.session['team1payRoll_beforeTrade'] = team1_payRoll
    request.session['team2payRoll_beforeTrade'] = team2_payRoll

    # Subtracting salaries of playing going away from team and then adding
    # salaries of players coming to teams
    # I know the variable names are confusing sorry
    team1_payRoll -= team1_sum_salary
    team2_payRoll -= team2_sum_salary

    team1_payRoll += team2_sum_salary
    team2_payRoll += team1_sum_salary

    team1_overcap = False
    team2_overcap = False

    # Adding more stuff to session
    request.session['team1payRoll_afterTrade'] = team1_payRoll
    request.session['team2payRoll_afterTrade'] = team2_payRoll
    request.session['cap'] = 99093000

    # Checking if any team is over cap
    if team1_payRoll > 99093000:
        team1_overcap = True
    if team2_payRoll > 99093000:
        team1_overcap = True

    # If neither teams are over cap then it's successful
    if not team1_overcap and not team2_overcap:
        response = {'status': 1}
        return HttpResponse(json.dumps(response), content_type='application/json')

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


    #setting all the trading list ids just dummy IDS
    if 'trade_history' in request.session:
        trade_history=request.session['trade_history']
        trade_history=json.loads(trade_history)
        trade_history.append(str(uuid.uuid4()))
        request.session['trade_history'] = json.dumps(trade_history)
    else:
        trade_history=list()
        trade_history.append(str(uuid.uuid4()))
        request.session['trade_history']=json.dumps(trade_history)


    #save the list of players in the session
    request.session['list1']=json.dumps(trade_options1)
    request.session['list2'] = json.dumps(trade_options2)
    print(trade_options1)
    print(trade_options2)
    return HttpResponse(json.dumps(response), content_type='application/json')

# If test fails this will be called
def failure(request):
    # Getting all our data from session
    team1 = request.session['team1']
    team2 = request.session['team2']

    team1payRoll_beforeTrade = request.session['team1payRoll_beforeTrade']
    team2payRoll_beforeTrade = request.session['team2payRoll_beforeTrade']

    team1payRoll_afterTrade = request.session['team1payRoll_afterTrade']
    team2payRoll_afterTrade = request.session['team2payRoll_afterTrade']


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

    '''
    return render(request, 'failure.html', {'team1': team1, 'team2': team2, 'team1payRoll_beforeTrade': team1payRoll_beforeTrade,\
                                            'team2payRoll_beforeTrade': team2payRoll_beforeTrade, 'team1payRoll_afterTrade': team1payRoll_afterTrade,\
                                            'team2payRoll_afterTrade': team2payRoll_afterTrade})
    '''
    return render(request, 'failure.html', locals())


# If test succeeds this will be called
def success(request):
    # Getting all our data from session
    team1 = request.session['team1']
    team2 = request.session['team2']

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
    team1payRoll_beforeTrade = request.session['team1payRoll_beforeTrade']
    team2payRoll_beforeTrade = request.session['team2payRoll_beforeTrade']

    team1payRoll_afterTrade = request.session['team1payRoll_afterTrade']
    team2payRoll_afterTrade = request.session['team2payRoll_afterTrade']

    ''' 
    return render(request, 'success.html', {'team1': team1, 'team2': team2, 'team1payRoll_beforeTrade': team1payRoll_beforeTrade,\
                                            'team2payRoll_beforeTrade': team2payRoll_beforeTrade, 'team1payRoll_afterTrade': team1payRoll_afterTrade,\
                                            'team2payRoll_afterTrade': team2payRoll_afterTrade})
    '''


    return render(request,'success.html',locals())



# MY API CALLS
# @csrf_exempt to disable csrf for this function.

# function will return the json list of players within the selected team.
@csrf_exempt
def get_player_by_team(request):
    team_id=request.POST.get("team_id") # get the team id which is selected
    teams=Team.objects.all().filter(id=team_id)  # to get Team Name
    for team in teams:
        team_name=team.teamName

    players=Player.objects.all().filter(playerTeam_id=team_id) # get all players in a selected team
    json_resp=[] # prepare a json array
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
    print(resp)
    return HttpResponse(resp) #send json response to ajax call

# @csrf_exempt to disable csrf for this function.

# function will return the json detail of  a player .

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
    print(resp)
    return HttpResponse(resp) #send json response to ajax call

@csrf_exempt
def get_player_stuff_test(request):
    player_list=request.POST.getlist('player_list[]')
    json_resp = []
    print ("player_list:"+str(player_list))
    print ("type(player_list):"+str(type(player_list)))
    for p in player_list:
        print ("p: "+str(p))
        player = Player.objects.get(playerName=p)
        obj = {}
        obj['id'] = player.id
        obj['playerName'] = player.playerName
        json_resp.append(obj)

    # players=Player.objects.filter(id=player_id).first()
    # json_resp = []
    # for player in players:
    #     obj = {}
    #     obj['id'] = player.id
    #     obj['playerName'] = player.playerName
    #     obj['playerTeam_id'] = player.playerTeam_id
    #     json_resp.append(obj)
    resp = json.dumps(json_resp)
    print(resp)
    return HttpResponse(resp) #send json response to ajax call