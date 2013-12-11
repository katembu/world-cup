from django.conf.urls import patterns, include, url

urlpatterns = patterns('tournament.views',
                       url(r'^$', 'index'),
                       url(r'^brackets/$', 'brackets'),
                       url(r'^brackets/(?P<bracket_name>.+)/$', 'brackets'),
                       url(r'^groups/$', 'group_create'),
                       url(r'^save/$', 'save'),
                       url(r'^about/$', 'about'),
                       )
