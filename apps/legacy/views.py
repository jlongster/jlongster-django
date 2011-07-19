from django.http import HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from os import path

def redirect(request, url):
    return HttpResponsePermanentRedirect(url)

def render_page(request, url):
    """ Take an old url and display the version we've cached """

    # Resolve paths of current directory and template
    current_dir = path.dirname(__file__)
    template = 'legacy/%s' % url.replace('/', '-')
    template_path = path.join(current_dir, 'templates', template)

    # Check if the file exists (better security & errors)
    if path.isfile(template_path):
        return render_to_response(template)
    return HttpResponseNotFound("not found")
