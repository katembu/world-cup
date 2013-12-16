from django.conf.urls import patterns, include, url

urlpatterns = patterns('tournament.views',
                       url(r'^$', 'brackets'),
                       url(r'^brackets/$', 'brackets'),
                       url(r'^brackets/(?P<bracket_name>.+)/$', 'render_bracket'),
                       url(r'^groups/$', 'groups'),
                       url(r'^groups/(?P<group_name>.+)/$', 'groups'),
                       url(r'^message/(?P<group_name>.+)/$', 'message_group'),
                       url(r'^login/(?P<group_name>.+)/$', 'group_login'),
                       url(r'^save/$', 'save'),
                       url(r'^about/$', 'about'),
                       )
