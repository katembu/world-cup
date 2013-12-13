from django.conf.urls import patterns, include, url

urlpatterns = patterns('tournament.views',
                       url(r'^$', 'index'),
                       url(r'^brackets/$', 'brackets'),
                       url(r'^brackets/(?P<bracket_name>.+)/$', 'brackets'),
                       url(r'^groups/$', 'groups'),
                       url(r'^groups/(?P<group_name>.+)/$', 'groups'),
                       url(r'^login/(?P<group_name>.+)/$', 'group_login'),
                       url(r'^save/$', 'save'),
                       url(r'^about/$', 'about'),
                       )
