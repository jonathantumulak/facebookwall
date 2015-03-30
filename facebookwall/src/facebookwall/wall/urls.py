from django.conf.urls import patterns, url
from wall import views

urlpatterns = patterns(
    '',
    url(r'^$', views.MyIndexView.as_view(), name='index'),
    url(r'^delete_status/$', views.DeleteStatus.as_view(), name='delete_status'),
    url(r'^(\d+)/delete_status/$', views.DeleteStatus.as_view(), name='delete_status'),
    url(r'^like_status/$', views.LikeStatus.as_view(), name='like_status'),
    url(r'^load_reply/$', views.ReplyView.as_view(),
        name='load_reply'),
    url(r'^load_reply_to_index/$', views.ReplyFromIndexView.as_view(),
        name='load_reply_to_index'),
    url(r'^(?P<pk>\d+)/$', views.MyDetailView.as_view(), name='detail'),
    url(r'^reply_detail/(?P<pk>\d+)/$', views.ReplyDetail.as_view(),
        name='reply_detail'),
    url(r'^status_detail/(?P<pk>\d+)/$', views.StatusDetail.as_view(),
        name='status_detail'),
    url(r'^edit_status/(?P<pk>\d+)$', views.StatusUpdateView.as_view(), name='edit_status'),
    url(r'^(\d+)/edit_status/(?P<pk>\d+)$', views.StatusUpdateView.as_view(), name='edit_status'),
)
