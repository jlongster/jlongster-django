from ablog.forms import PostForm
from models import TechPost

class TechPostForm(PostForm):
    class Meta:
        model = TechPost

    def clean(self):
        tagstr = self.cleaned_data.get('tagstr', '')

        # Automatically add the "tech" tag
        tagstr = ','.join(tagstr.split(',') + ['tech'])
        self.cleaned_data['tagstr'] = tagstr

        return super(TechPostForm, self).clean()
