from os.path import join

from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from views import home, contact
from legacy.urls import legacy_urls

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', home),
    (r'^contact/', contact),

    (r'^blog/', include('ablog.urls')),
    (r'^tech/', include('tech.urls')),
    (r'^legacy/', include('legacy.urls')),
    (r'^docs/', include('docs.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns = legacy_urls + urlpatterns

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
