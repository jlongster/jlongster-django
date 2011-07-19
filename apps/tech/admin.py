from django.contrib import admin
from ablog.admin import PostAdmin
from models import TechPost
from forms import TechPostForm

class TechPostAdmin(PostAdmin):
    readonly_fields = ['updated_date']
    form = TechPostForm

admin.site.register(TechPost, TechPostAdmin)
