from django.conf.urls import patterns, url, include
from . import views  # 从social包中导入views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    # main page
    url(r'^$', views.index, name='index'),
    # signup page
    url(r'^signup/$', views.signup, name='signup'),
    # register new user
    url(r'^register/$', views.register, name='register'),
    # login page
    url(r'^login/$', views.login, name='login'),
    # logout page
    url(r'^logout/$', views.logout, name='logout'),
    # members page
    url(r'^members/$', views.members, name='members'),
    # friends page
    url(r'^friends/$', views.friends, name='friends'),
    # user profile edit page
    url(r'^profile/$', views.profile, name='profile'),
    # Ajax: check if user exists
    url(r'^checkuser/$', views.checkuser, name='checkuser'),
    # messages page
    url(r'^messages/$', views.message, name='messages'),
    # rest api
    url(r'^api/$', views.snippet_list),
    url(r'^messages/(?P<username>\w+)/$', views.snippet_detail)
    )

urlpatterns = format_suffix_patterns(urlpatterns)



