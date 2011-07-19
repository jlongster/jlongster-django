from django.conf.urls.defaults import *
from views import render_page, redirect

urlpatterns = patterns('',
    (r'(.*)', render_page)
)

legacy_urls = patterns('',
    (r'^blog/2009/06/17/write-apps-iphone-scheme/$', redirect,
     { 'url':'/legacy/scheme-iphone-apps.html' }),
    (r'^blog/2010/02/08/fonts-ugh/$', redirect,
     { 'url':'/legacy/fonts-ugh.html' }),
    (r'^blog/2009/07/05/remotely-debugging-iphone-scheme/$', redirect,
     { 'url':'/legacy/remotely-debugging-iphone-scheme.html' }),
    (r'^software/iphone/scheme-iphone-example/$', redirect,
     { 'url':'/legacy/scheme-iphone-example.html' }),
    (r'^mozilla$', redirect,
     { 'url':'/blog/mozilla' })
)
