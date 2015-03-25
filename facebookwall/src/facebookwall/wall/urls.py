from django.conf.urls import patterns, url
from wall import views

urlpatterns = patterns(
    '',
    url(r'^$', views.MyIndexView.as_view(), name='index'),
    url(r'^delete_status/$', views.delete_status, name='delete_status'),
    url(r'^like_status/$', views.like_status, name='like_status'),
    url(r'^edit_status/$', views.edit_status, name='edit_status'),
    url(r'^(?P<pk>\d+)/$', views.MyDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit_status/$', views.edit_status, name='edit_status'),
)
