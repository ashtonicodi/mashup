'''Preview for entry'''
from collections import deque

from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.text import Truncator

from bs4 import BeautifulSoup

from blog.settings import PREVIEW_MAX_WORDS
from blog.settings import PREVIEW_MORE_STRING
from blog.settings import PREVIEW_SPLITTERS


class HTMLPreview:
    '''
    Build an HTML preview of an HTML content.
    '''
    def __init__(self, content,
                 splitters=PREVIEW_SPLITTERS,
                 max_words=PREVIEW_MAX_WORDS,
                 more_string=PREVIEW_MORE_STRING):
        self._preview = None

        self.content = content
        self.splitters = splitters
        self.max_words = max_words
        self.more_string = more_string

    @property
    def preview(self):
        '''
        The preview is a cached property.
        '''
        if self._preview is None:
            self._preview = self.build_preview()
        return self._preview

    @property
    def has_more(self):
        '''
        Boolean telling if the preview has hidden content.
        '''
        return bool(self.content and self.preview != self.content)

    def __str__(self):
        return self.preview

    def build_preview(self):
        '''
        Build the preview by:

        - Returning the lead attribute if not empty.
        - Checking if a split marker is present in the content
          Then split the content with the marker to build the preview.
        - Splitting the content to a fixed number of words.
        '''
        for splitter in self.splitters:
            if splitter in self.content:
                return self.split(splitter).get_text()
        return self.truncate()

    def truncate(self):
        '''
        Truncate the content with the Truncator object.
        '''
        return Truncator(self.content).words(
            self.max_words, self.more_string, html=True
        )

    def split(self, splitter):
        '''
        Split the HTML content with a marker
        without breaking closing markups.
        '''
        soup = BeautifulSoup(self.content.split(splitter)[0],
                             'html.parser')
        last_string = soup.find_all(text=False)[-1]
        last_string.replace_with(last_string.string + self.more_string)
        return soup

    def alter_split(self, splitter):
        pass

    @cached_property
    def total_words(self):
        '''
        Return the total of words contained
        in the content and in the lead.
        '''
        return len(strip_tags(self.content).split())

    @cached_property
    def displayed_words(self):
        '''
        Returns the number of words displayed in the preview.
        '''
        return len(strip_tags(self.preview).split())

    @cached_property
    def remaining_words(self):
        '''
        Return the number of words remaining after the preview.
        '''
        return self.total_words - self.displayed_words

    @cached_property
    def displayed_percent(self):
        '''
        Return the percentage of the content displayed in the preview.
        '''
        return round((self.displayed_words / self.total_words) * 100, 2)

    @cached_property
    def remaining_percent(self):
        '''
        Return the percentage of the content remaining after the preview.
        '''
        return round((self.remaining_words / self.total_words) * 100, 2)