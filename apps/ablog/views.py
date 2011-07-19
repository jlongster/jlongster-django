from django.http import HttpResponse
import jingo
import helpers
from models import Post, Tag

def index(request):
    posts = Post.objects.posts()
    return jingo.render(request, 'ablog/home.html',
                        {'posts': posts})

def view_post(request, year, month, slug):
    qs = (Post.objects.posts()
                       .filter(created_date__year=year)
                       .filter(created_date__month=month)
                       .filter(slug=slug)
                       .filter(in_blog=True))

    post = None
    if qs.exists():
        post = qs[0]

    return jingo.render(request, 'ablog/post.html',
                        {'post': post},
                        status=200 if post else 404)

def view_tag(request, tag):
    posts = Post.objects.posts().with_tags(tag)
    return jingo.render(request, 'ablog/tag.html',
                        {'posts': posts,
                         'tag': tag})

