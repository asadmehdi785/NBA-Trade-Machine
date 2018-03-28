from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from mysite.core import views as core_views

#admin.autodiscover()
urlpatterns = [
	#url(r'^trade/$',core_views.home,name=' home'),
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
	url(r'^trade/$', core_views.trade, name='trade'),
	url(r'^result/$', core_views.result, name='result'),
	url(r'^failure/$', core_views.failure, name='failure'),
	url(r'^admin/', admin.site.urls),
]
