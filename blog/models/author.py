from django.db import models
from django.apps import apps
from django.conf import settings

from blog.managers import EntryRelatedPublishedManager
from blog.managers import entries_published


def safe_get_user_model():
    '''
    Safe loading of the User model, customized or not.
    '''
    user_app, user_model = settings.AUTH_USER_MODEL.split('.')
    return apps.get_registered_model(user_app, user_model)


class AuthorPublishedManager(models.Model):
    '''
    Proxy model manager to avoid overriding of
    default User's manager.
    '''
    published = EntryRelatedPublishedManager()

    class Meta:
        abstract = True


class Author(safe_get_user_model(),
             AuthorPublishedManager):
    '''
    Proxy model around :class:'django.contrib.auth.models.get_user_model'.
    '''
    def entries_published(self):
        '''
        Returns author's published entries.
        '''
        return entries_published(self.entries)

    @models.permalink
    def get_absolute_url(self):
        '''
        Builds and returns the author's URL based on his user name.
        '''
        return ('blog:author_detail', (self.get_username(),))

    def __str__(self):
        '''
        If the user has a full name, use it instead of the user name.
        '''
        return self.get_full_name() or self.get_username()

    class Meta:
        proxy = True