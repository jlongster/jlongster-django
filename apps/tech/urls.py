from django.conf.urls.defaults import *
from views import home, view_post, view_tag

urlpatterns = patterns('',
    (r'^$', home),
    (r'^tag/(.*)/', view_tag),
    (r'^(.*)/$', view_post)
)
