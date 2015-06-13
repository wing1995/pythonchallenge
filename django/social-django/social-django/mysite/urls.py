from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^social/', include('social.urls')),  # 将新建的app中的urls.py加入其中
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/token/', obtain_auth_token, name='api-token')
)
