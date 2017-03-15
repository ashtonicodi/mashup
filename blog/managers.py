from django.db import models
from django.utils import timezone

DRAFT = 0
HIDDEN = 1
PUBLISHED = 2


def entries_published(queryset):
    '''
    Return only the entries published.
    '''
    now = timezone.now()
    return queryset.filter(
        models.Q(start_publication__lte=now) |
        models.Q(start_publication=None),
        models.Q(end_publication__gt=now) |
        models.Q(end_publication=None),
        status=PUBLISHED
    )


class EntryPublishedManager(models.Manager):
    '''
    Manager to retrieve published entries.
    '''

    def get_queryset(self):
        '''
        Return published entries.
        '''
        return entries_published(
            super(EntryPublishedManager, self).get_queryset()
        )


class EntryRelatedPublishedManager(models.Manager):
    '''
    Manager to retrieve objects associated with published entries.
    '''
    def get_queryset(self):
        '''
        Return a query set containing published entries.
        '''
        now = timezone.now()
        return super(
            EntryRelatedPublishedManager, self).get_queryset().filter(
            models.Q(entries__start_publication__lte=now) |
            models.Q(entries__start_publication=None),
            models.Q(entries__end_publication__gt=now) |
            models.Q(entries__end_publication=None),
            entries__status=PUBLISHED
        )