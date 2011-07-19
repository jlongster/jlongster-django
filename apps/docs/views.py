from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response
from os import path

def render_doc(request, url):
    """ Render a doc """

    current_dir = path.dirname(__file__)
    template = 'docs/%s' % url.replace('/', '-')
    template_path = path.join(current_dir, 'templates', template)

    # Check if the file exists (better security & errors)
    if path.isfile(template_path):
        return render_to_response(template)
    return HttpResponseNotFound("not found")
