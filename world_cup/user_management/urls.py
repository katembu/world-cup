from django.conf.urls import patterns, include, url

urlpatterns = patterns('user_management.views',
                       url(r'^$', 'index'),
                       url(r'^accounts/login/', 'login_user'),
                       url(r'^accounts/logout/', 'logout_user'),
                       url(r'^accounts/create/', 'create_user'),
                       url(r'^contact/', 'contact')
                       )
