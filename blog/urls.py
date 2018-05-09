from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    #post views
    #no arguments, mapped to post list view
    url(r'^$', views.post_list, name='post_list'),
    #url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    #takes arguments and mapped to post detail view
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
    #for sending emails
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),

]
