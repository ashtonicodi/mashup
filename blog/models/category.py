'''Category model for blog '''
from django.db import models
from django.utils.translation import ugettext_lazy as _

from blog.managers import EntryRelatedPublishedManager
from blog.managers import entries_published


class Category(models.Model):
    '''
    Simple model for categorizing entries.
    '''
    title = models.CharField(
        _('title'), max_length=255
    )

    slug = models.SlugField(
        _('slug'), unique=True, max_length=255,
        help_text=_('Used to build the category\'s URL.')
    )

    description = models.TextField(
        _('description'), blank=True
    )

    objects = models.Manager()
    published = EntryRelatedPublishedManager()

    def entries_published(self):
        '''
        Returns category's published entries.
        '''
        return entries_published(self.entries)

    @models.permalink
    def get_absolute_url(self):
        '''
        Builds and returns the category's URL
        based on his ID
        '''
        return ('blog:category_detail', (self.pk,))

    def __str__(self):
        return self.title

    class Meta:
        '''
        Category's meta information.
        '''
        ordering = ['title']
        verbose_name = _('category')
        verbose_name_plural = _('categories')