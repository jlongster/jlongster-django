from django.db import models


class QuerySetManager(models.Manager):
    def __init__(self, qs_class=models.query.QuerySet):
        self.queryset_class = qs_class
        super(QuerySetManager, self).__init__()

    def get_query_set(self):
        return self.queryset_class(self.model)

    def __getattr__(self, name, *args):
        # This is a fix described in 
        # https://code.djangoproject.com/ticket/15062
        if name.startswith("_"):
            raise AttributeError

        return getattr(self.get_query_set(), name, *args)
                
