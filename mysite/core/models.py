# This file defines the models that are used in the system. In Django, models
# are used to create objects in the database. For example, we have a Team model
# defined below. With this model, we can create an instance of a Team object, as
# long as we appropriately provide the 'teamName' and 'teamPayroll' fields.

from __future__ import unicode_literals
from django.db import models

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