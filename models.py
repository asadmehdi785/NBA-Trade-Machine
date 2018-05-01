# This file defines the models that are used in the system. In Django, models
# are used to create objects in the database. For example, we have a Team model
# defined below. With this model, we can create an instance of a Team object, as
# long as we appropriately provide the 'teamName' and 'teamPayroll' fields.

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

import datetime

# Team model
# 'teamName' refers to the name of the team.
# 'teamPayroll' refers to the payroll of the team.
# Additionally, we have defined a '__str__' method, which simply helps in 
# displaying what a particular team is when we try to print a particular
# instance from the shell.
class Team(models.Model):
	teamName = models.CharField(max_length=100)
	teamPayroll = models.IntegerField(default=500000)

	# Defining a method to return team name
	def __str__(self):
		return self.teamName

# Player model
# 'playerTeam' is a foreign key which maps the player to the team they are on.
# This essentially defines a 'many-to-one' relationship.
# 'playerName' is the name of the player.
# 'playerSalary' is the current salary of the player.
# 'playerppg' is the ppg (points per game) statistic for the player.
# 'playerrpg' is the rpg (rebounds per game) statistic for the player.
# 'playerapg' is the apg (assists per game) statistic for the player.
# Additionally, we have defined a '__str__' method for the same reason as given
# above.
class Player(models.Model):
	playerTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
	playerName = models.CharField(max_length=100)
	playerSalary = models.IntegerField(default=500000)
	playerppg = models.FloatField(default=10.5)
	playerrpg = models.FloatField(default=3.5)
	playerapg = models.FloatField(default=4.5)

	def __str__(self):
		return self.playerName

# Transaction model
# 'tradeID' is the unique identifier associated with the trade
# 'userID' is the unique identifier of the user who tested the trade
# 'date' is the date when the trade was made
# 'result' is either "success" or "failure"
# 'team1Name' is the name of the first team chosen
# 'team2Name' is the name of the second team chosen
# 'team3Name' is the name of the third team chosen
# 'team1PayrollBefore' is the payroll of team 1 before the trade was attempted
# 'team2PayrollBefore' is the payroll of team 2 before the trade was attempted
# 'team3PayrollBefore' is the payroll of team 3 before the trade was attempted
# 'team1PayrollAfter' is the payroll of team 1 after the trade was attempted
# 'team2PayrollAfter' is the payroll of team 2 after the trade was attempted
# 'team3PayrollAfter' is the payroll of team 3 after the trade was attempted
# Additionally, we have defined a '__str__' method for the same reason as given
# above.
class Transaction(models.Model):
	tradeId=models.CharField(max_length=255)
	userId=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateTimeField(default=datetime.datetime.now, blank=True)
	result=models.CharField(max_length=255)
	team1Name=models.CharField(max_length=255)
	team2Name = models.CharField(max_length=255)
	team3Name = models.CharField(max_length=255,blank=True)
	team1PayrollBefore=models.CharField(max_length=255)
	team2PayrollBefore = models.CharField(max_length=255)
	team3PayrollBefore = models.CharField(max_length=255,blank=True)
	team1PayrollAfter = models.CharField(max_length=255)
	team2PayrollAfter = models.CharField(max_length=255)
	team3PayrollAfter = models.CharField(max_length=255,blank=True)

	def __str__(self):
		return self.tradeId+str(self.userId_id)+str(self.result)

# TradingStrategy model-> to implement the Strategy Design Pattern
# SignAndTrade and NormalTrade are the two strategies implemented, overriding
#     the value functionality as needs be
# '_name' is an identifier for the given strategy interface
# 'strategy' denotes which strategy algorithm is to be run
class TradingStrategy(models.Model):
    _name = models.CharField(max_length=200)
    strategy = models.CharField(max_length=255)
    # used as a property
    def value():
        def fget(self):
            return self.strategy.value

class SignAndTrade(models.Model):
    def value():
        def fget(self):
            return 'sign-and-trade'

class NormalTrade(models.Model):
    def value():
        def fget(self):
        	return 'normal'

# History model
# 'team' is the team associated with the trade
# 'tradeID' is the unique identifer associated with the trade
# 'playerName' is the name of the player associated with the team
# Additionally, we have defined a '__str__' method for the same reason as given
# above.
class History(models.Model):
	team=models.CharField(max_length=255)
	tradeId=models.ForeignKey(Transaction,on_delete=models.CASCADE)
	playerName=models.CharField(max_length=255)

	def __str__(self):
		return self.tradeId+str(':')+str(self.team)
