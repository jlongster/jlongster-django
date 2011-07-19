from django.conf.urls.defaults import *
from views import index, view_post, view_tag

urlpatterns = patterns('',
    (r'^$', index),
    (r'^tag/(.*)/', view_tag),
    (r'^(\d+)/(\d+)/(.+)/', view_post),
)
