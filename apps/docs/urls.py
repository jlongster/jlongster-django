from django.conf.urls.defaults import *
from views import render_doc

urlpatterns = patterns('',
    (r'(.*)', render_doc)
)
