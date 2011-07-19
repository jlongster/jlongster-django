from django.forms import ModelForm, CharField
from models import Post, Tag, SPECIAL_SECTIONS

class PostForm(ModelForm):
    class Meta:
        model = Post

    tagstr = CharField(max_length=1024, label="Tags", required=False)
