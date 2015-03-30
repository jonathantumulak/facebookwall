from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic.edit import CreateView
import views
# from django.contrib.auth.forms import UserCreationForm
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    # url('^', include('django.contrib.auth.urls')),
    url(r'^$', 'facebook_wall.views.index'),
    url(r'^login/$', login,
        {'template_name': 'login.html'}),
    url(r'^logout/$', logout,
        {'template_name': 'logout.html'}),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^wall/', include('wall.urls', namespace="wall")),
)
