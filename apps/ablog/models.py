from os.path import join
from datetime import date

from django.db import models

import util

SPECIAL_SECTIONS = ['tech']

class PostQuerySet(models.query.QuerySet):
    def published(self):
        return self.filter(published=True).order_by('-published_date')

    def with_tags(self, *tags):
        qs = self
        for tag in tags:
            qs = qs.filter(tags__name=tag)
        return qs

    def without_tags(self, *tags):
        qs = self
        for tag in tags:
            qs = qs.exclude(tags__name=tag)
        return qs

    def posts(self, *tags):
        return self.filter(in_blog=True).with_tags(*tags).published()

    @classmethod
    def as_manager(cls):
        return util.QuerySetManager(qs_class=cls)

class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=1024, blank=True)
    created_date = models.DateField(auto_now_add=True)
    published_date = models.DateField(blank=True, null=True)
    published = models.BooleanField()
    abstract = models.TextField()
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    tagstr = models.CharField(max_length=1024)
    in_blog = models.BooleanField(default=True)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def url(self, base_url='/blog/'):
        tags = self.tagstr.split(',')

        for tag in tags:
            if tag.strip() in SPECIAL_SECTIONS:
                return join('/', tag, self.slug)
        
        return join(base_url,
                    '%s/%s/%s' % (self.created_date.year,
                                  self.created_date.month,
                                  self.slug))

    def save(self, *args, **kwargs):
        if self.published and not self.published_date:
            self.published_date = date.today()

        super(Post, self).save(*args, **kwargs)
