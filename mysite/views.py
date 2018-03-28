# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

@login_required
def home(request):
	return HttpResponseRedirect(
		reverse(NAME_OF_PROFILE_VIEW, args[request.user.username])
	)

def index(request):
	return render(request, 'templates/index.html')

def trade(request):
	return render(request, 'templates/trade.html')

