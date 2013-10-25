from django.conf.urls import patterns, include, url

urlpatterns = patterns('user_management.views',
                       url(r'^$', 'index'),
                       url(r'^login/', 'login_user'),
                       url(r'^create/', 'create_user'),
                       )
