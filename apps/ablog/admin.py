from django.contrib import admin
from django.forms import TextInput
from models import Post, Tag, SPECIAL_SECTIONS
from forms import PostForm

class PostAdmin(admin.ModelAdmin): 
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('tags','in_blog')
    form = PostForm

    def save_model(self, request, obj, form, change):
        obj.save()

        tagstr = form.cleaned_data['tagstr']
        tags = [x.strip().lower() for x in tagstr.split(',')]
        tags = [x for x in tags if x]

        # Update the tag relationships
        tagset = []
        for tag in tags:
            qs = Tag.objects.filter(name=tag)

            if qs.exists():
                tagobj = qs[0]
            else:
                tagobj = Tag.objects.create(name=tag)

            if obj not in tagset:
                tagset.append(tagobj)

        obj.tags.clear()
        for tag in tagset:
            obj.tags.add(tag)

        # Update the tagstr
        obj.tagstr = ', '.join([tag.name for tag in tagset])

        # Cache if the post is included in the default blog set
        for tag in tagset:
            if tag.name in SPECIAL_SECTIONS:
                obj.in_blog = False

        print obj.in_blog
        obj.save()

admin.site.register(Post, PostAdmin)
