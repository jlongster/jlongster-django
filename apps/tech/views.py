from django.http import HttpResponse
import jingo
import helpers
from models import TechPost

def home(request):
    posts = TechPost.objects.posts()
    return jingo.render(request, 'tech/home.html',
                        {'posts': posts})

def view_post(request, slug):
    qs = TechPost.objects.posts().filter(slug=slug)
    post = None

    if qs.exists():
        post = qs[0]

    return jingo.render(request, 'tech/post.html',
                        {'post': post},
                        status=200 if post else 404)

def view_tag(request, tag):
    posts = TechPost.objects.posts().with_tags(tag)
    return jingo.render(request, 'tech/tag.html',
                        {'posts': posts,
                         'tag': tag})
