from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Team(models.Model):
	teamName = models.CharField(max_length=100)
	teamPayroll = models.IntegerField(default=500000)

	# Defining a method to return team name
	def __str__(self):
		return self.teamName

class Player(models.Model):
	playerTeam = models.ForeignKey(Team, on_delete=models.CASCADE)
	playerName = models.CharField(max_length=100)
	playerSalary = models.IntegerField(default=500000)
	playerppg = models.FloatField(default=10.5)
	playerrpg = models.FloatField(default=3.5)
	playerapg = models.FloatField(default=4.5)

	def __str__(self):
		return self.playerName