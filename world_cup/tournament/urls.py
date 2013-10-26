from django.conf.urls import patterns, include, url

urlpatterns = patterns('tournament.views',
                       url(r'^$', 'index'),
                       url(r'^brackets/$', 'brackets'),
                       url(r'^brackets/save/$', 'save'),
                       )
