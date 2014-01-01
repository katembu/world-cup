from django.conf.urls import patterns, include, url

urlpatterns = patterns('user_management.views',
                       url(r'^$', 'index'),
                       url(r'^accounts/login/$', 'login_user'),
                       url(r'^accounts/logout/$', 'logout_user'),
                       url(r'^accounts/create/$', 'create_user'),
                       url(r'^contact/$', 'contact'),
                       url(r'^tipjar/$', 'donate'),
                       url(r'^messages/$', 'messages'),
                       url(r'^message/form/$', 'message_form'),
                       url(r'^message/send/$', 'message_send'),
                       url(r'^message/delete/$', 'message_delete'),
                       url(r'^userlist/$', 'user_list'),
                       url(r'^profile/$', 'user_profile'),
                       url(r'^unsubscribe/$', 'unsubscribe'),
                       )
