# This file details what models are available to be viewed via the admin panel.

# A superuser can edit fields for any given object directly from the admin panel.

from django.contrib import admin
from .models import Team, Player, Transaction, History

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Transaction)
admin.site.register(History)