
from django.db import models
from django.db.models import Q


# Search Managers
class ServiceManager(models.Manager):

    def search(self, query=None):
        """
        Define a search function for query to call and returns proper results.
        :param query:
        :return: QuerySet
        """
        from .utils import str2date
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(description__icontains=query) |
                         Q(note__icontains=query) |
                         Q(service_date=str2date(query)))
            qs = qs.filter(or_lookup).distinct()
        return qs


class GroupAndCategoryManager(models.Manager):

    def search(self, query=None):
        """
        Define a search function for query to call and returns proper results.
        :param query:
        :return: QuerySet
        """
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(description__icontains=query) |
                         Q(name__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs