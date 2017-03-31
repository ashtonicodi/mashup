import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _

from blog.managers import DRAFT, HIDDEN, PUBLISHED
from blog.managers import EntryPublishedManager
from blog.contrib import HTMLPreview
from blog.utils import generate_filename
from blog.settings import UPLOAD_TO

# Create your models here.
class CoreEntry(models.Model):
    """
    Abstract core entry model class providing
    the fields and methods required for publishing
    content over time.
    """
    STATUS_CHOICES = (
        (DRAFT, _('draft')),
        (HIDDEN, _('hidden')),
        (PUBLISHED, _('published')),
    )

    title = models.CharField(
        _('Title'), max_length=255
    )

    status = models.IntegerField(
        _('status'), db_index=True,
        choices=STATUS_CHOICES, default=DRAFT
    )

    publication_date = models.DateTimeField(
        _('publication date'),
        db_index=True, default=timezone.now,
        help_text=_("Used to build the entry's URL."))

    start_publication = models.DateTimeField(
        _('start publication'),
        db_index=True, blank=True, null=True,
        help_text=_('Start date of publication.'))

    end_publication = models.DateTimeField(
        _('end publication'),
        db_index=True, blank=True, null=True,
        help_text=_('End date of publication.'))

    creation_date = models.DateTimeField(
        _('creation date'), default=timezone.now
    )

    last_update = models.DateTimeField(
        _('last update'), default=timezone.now
    )

    objects = models.Manager()
    published = EntryPublishedManager()

    @property
    def is_actual(self):
        '''
        Check if an entry is within his publication period.
        '''
        now = timezone.now()
        if self.start_publication and now < self.start_publication:
            return False

        if self.end_publication and now >= self.end_publication:
            return False
        return True

    @property
    def is_visible(self):
        '''
        Check if an entry is visible and published.
        '''
        now = timezone.now()
        return self.is_actual and self.status == PUBLISHED

    def save(self, *args, **kwargs):
        '''
        Overrides the save method to update
        the last_update field.
        '''
        self.last_update = timezone.now()
        super(CoreEntry, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        '''
        Builds and returns the entry's URL based on
        the ID.
        '''
        return ('entry_detail', (self.pk,))

    def __str__(self):
        return '%s: %s' % (self.title, self.get_status_display())


    class Meta:
        '''
        Entry's meta information
        '''
        abstract = True

        verbose_name = _('entry')
        verbose_name_plural = _('entries')

        ordering = ['-publication_date']
        get_latest_by = 'publication_date'

        index_together = [
            ['status', 'publication_date'],
            ['start_publication', 'end_publication'],
        ]

        permissions = (
            ('can_view_all', _('Can view all entries')),
            ('can_change_status', _('Can change status')),
            ('can_change_author', _('Can change author(s)')),
        )


class ContentEntry(models.Model):
    '''
    Abstract content model class providing field
    and methods to write content inside an entry.
    '''
    content = models.TextField(_('content'), blank=True)

    @property
    def html_content(self):
        '''
        Returns the "content" field formatted in HTML.
        '''
        return self.content

    @property
    def html_preview(self):
        '''
        Returns a preview of the "content" field,
        formatted in HTML.
        '''
        return HTMLPreview(self.html_content)

    @property
    def word_count(self):
        '''
        Counts the number of words used in the contents.
        '''
        return len(strip_tags(self.html_content).split())

    class Meta:
        abstract = True


def image_upload_to_dispatcher(entry, filename):
    """
    Dispatch function to allow overriding of ``image_upload_to`` method.
    """
    return entry.image_upload_to(filename)


class ImageEntry(models.Model):
    """
    Abstract model class to add an image for illustrating the entries.
    """

    def image_upload_to(self, filename):
        """
        Compute the upload path for the image field.
        """
        now = timezone.now()
        _f, extension = os.path.splitext(filename)

        filename = generate_filename(prefix='cover')

        return os.path.join(
            UPLOAD_TO,
            now.strftime('%Y'),
            now.strftime('%m'),
            now.strftime('%d'),
            '%s%s' % (filename, extension))

    image = models.ImageField(
        _('image'), blank=True,
        upload_to=image_upload_to_dispatcher,
        help_text=_('Used for illustration.'))

    image_caption = models.TextField(
        _('caption'), blank=True,
        help_text=_("Image's caption."))

    class Meta:
        abstract = True


class FeaturedEntry(models.Model):
    """
    Abstract model class to mark entries as featured.
    """
    featured = models.BooleanField(
        _('featured'), default=False)

    class Meta:
        abstract = True


class AuthorsEntry(models.Model):
    """
    Abstract model class to add relationship
    between the entries and their authors.
    """
    authors = models.ManyToManyField(
        'blog.Author',
        blank=True,
        related_name='entries',
        verbose_name=_('authors'))

    class Meta:
        abstract = True


class CategoriesEntry(models.Model):
    """
    Abstract model class to categorize the entries.
    """
    categories = models.ManyToManyField(
        'blog.Category',
        blank=True,
        related_name='entries',
        verbose_name=_('categories'))

    class Meta:
        abstract = True


class LoginRequiredEntry(models.Model):
    """
    Abstract model class to restrict the display
    of the entry on authenticated users.
    """
    login_required = models.BooleanField(
        _('login required'), default=False,
        help_text=_('Only authenticated users can view the entry.'))

    class Meta:
        abstract = True


class AbstractEntry(
        CoreEntry,
        ContentEntry,
        ImageEntry,
        FeaturedEntry,
        AuthorsEntry,
        CategoriesEntry,
        LoginRequiredEntry):
    """
    Final abstract entry model class assembling
    all the abstract entry model classes into a single one.

    In this manner we can override some fields without
    reimplementing all the AbstractEntry.
    """

    class Meta(CoreEntry.Meta):
        abstract = True