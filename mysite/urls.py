from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from mysite.core import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^about_us/$', core_views.about_us, name='about_us'),
    url(r'^privacy/$', core_views.privacy, name='privacy'),
    url(r'^terms/$', core_views.terms, name='terms'),
    url(r'^rules/$', core_views.rules, name='rules'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
	url(r'^trade/$', core_views.trade, name='trade'),
	url(r'^test_trade/$', core_views.test_trade, name='test_trade'),
	url(r'^failure/$', core_views.failure, name='failure'),
    url(r'^success/$', core_views.success, name='success'),
    url(r'^trade_history/$', core_views.trade_history, name='trade_history'),#trade history page
    url(r'^trade_result/$', core_views.trade_result, name='trade_result'), #details of a single trade id
    url(r'^admin/', admin.site.urls),
    url(r'^get_player_by_team',core_views.get_player_by_team),
    url(r'^get_player_info', core_views.get_player_info)
]
