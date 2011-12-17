from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^', include('core.urls')),
    url(r'auth/', include('account.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()