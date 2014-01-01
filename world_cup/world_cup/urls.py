from django.conf import settings
from django.http import HttpResponse
from django.conf.urls import patterns, include, url, static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       #url(r'^$', 'world_cup.views.home', name='home'),
                       url(r'^', include('user_management.urls')),
                       url(r'^tournament/', include('tournament.urls')),
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", mimetype="text/plain"))
                       )

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
