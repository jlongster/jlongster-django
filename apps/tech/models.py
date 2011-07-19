from datetime import date
from django.db import models
from ablog.models import Post, PostQuerySet

class TechPostQuerySet(PostQuerySet):
    def with_tags(self, *tags):
        tags = list(tags)
        tags.append('tech')
        return super(TechPostQuerySet, self).with_tags(*tags)

    def without_tags(self, *tags):
        qs = super(TechPostQuerySet, self).without_tags(*tags)
        return qs.with_tags('tech')

    def posts(self, *tags):
        return self.with_tags(*tags).published()

class TechPost(Post):
    updated_date = models.DateField()
    objects = TechPostQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.updated_date = date.today()

        super(TechPost, self).save(*args, **kwargs)
