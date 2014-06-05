from django.conf.urls import patterns, url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = patterns('user_management.views',
                       url(r'^$', 'index'),
                       url(r'^accounts/login/$', 'login_user'),
                       url(r'^accounts/logout/$', 'logout_user'),
                       url(r'^accounts/create/$', 'create_user'),
                       url(r'^accounts/password/reset/$', password_reset,
                           {'post_reset_redirect': '/accounts/password/reset/done/'}, name="password_reset"),
                       url(r'^accounts/password/reset/done/$', password_reset_done),
                       url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           password_reset_confirm, {'post_reset_redirect': '/accounts/password/done/'},
                           name="password_reset_confirm"),
                       url(r'^accounts/password/done/$', password_reset_complete),
                       url(r'^messages/$', 'messages'),
                       url(r'^message/form/$', 'message_form'),
                       url(r'^message/send/$', 'message_send'),
                       url(r'^message/delete/$', 'message_delete'),
                       url(r'^userlist/$', 'user_list'),
                       url(r'^profile/$', 'user_profile'),
                       url(r'^unsubscribe/$', 'unsubscribe'),
                       )
