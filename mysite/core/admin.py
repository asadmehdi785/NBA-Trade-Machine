# This file details what models are available to be viewed via the admin panel.
# Currently, both the Team and Player models are made available. This means that
# a user defined as a superuser may enter into the admin panel and view all the
# Team and Player objects stored in the database. Additionally, a superuser can
# edit fields for any given object directly from the admin panel.

from django.contrib import admin
from .models import Team, Player

admin.site.register(Team)
admin.site.register(Player)