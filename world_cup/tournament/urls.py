from django.conf.urls import patterns, include, url

urlpatterns = patterns('tournament.views',
                       url(r'^$', 'brackets'),
                       url(r'^brackets/$', 'brackets'),
                       url(r'^brackets/(?P<bracket_name>.+)/$', 'render_bracket'),
                       url(r'^groups/$', 'groups'),
                       url(r'^groups/(?P<group_name>.+)/$', 'groups'),
                       url(r'^invite/(?P<group_name>.+)/$', 'send_invites'),
                       url(r'^login/(?P<group_name>.+)/$', 'group_login'),
                       url(r'^leavegroup/', 'leave_group'),
                       url(r'^save/$', 'save'),
                       url(r'^reset/$', 'reset'),
                       url(r'^about/$', 'about'),
                       url(r'^usa/$', 'usa'),
                       )
