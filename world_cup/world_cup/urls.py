from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^$', 'world_cup.views.home', name='home'),
                       url(r'^', include('user_management.urls')),
                       url(r'^tournament/', include('tournament.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
