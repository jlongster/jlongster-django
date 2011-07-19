import jingo
from ablog.models import Post
from tech.models import TechPost

def home(request):
    posts = Post.objects.posts()[:3]
    tech_posts = TechPost.objects.posts()[:3]
    return jingo.render(request, 'home.html',
                        {'posts': posts,
                         'tech_posts': tech_posts})

def contact(request):
    return jingo.render(request, 'contact.html')
