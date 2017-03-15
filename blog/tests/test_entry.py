from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.utils.translation import activate
from django.utils.translation import deactivate

from blog.models import Entry
from blog.managers import PUBLISHED
from blog.settings import PREVIEW_MAX_WORDS
from blog.settings import PREVIEW_MORE_STRING
from blog.tests.utils import datetime


class EntryTestCase(TestCase):

    def setUp(self):
        params = {
            'title': 'My entry',
            'content': 'My content',
        }
        self.entry = Entry.objects.create(**params)

    def test_str(self):
        activate('en')
        self.assertEqual(str(self.entry), 'My entry: draft')
        deactivate()

    def test_word_count(self):
        self.assertEqual(self.entry.word_count, 2)
        html_content = (
            '<h1>HTML entry</h1> <br> '
            '<p>Entry description</p>'
        )
        self.entry.content = html_content
        self.entry.save()
        self.assertEqual(self.entry.word_count, 4)

    def test_is_actual(self):
        self.assertTrue(self.entry.is_actual)

        self.entry.start_publication = datetime(2020, 3, 15)
        self.assertFalse(self.entry.is_actual)

        self.entry.start_publication = timezone.now()
        self.assertTrue(self.entry.is_actual)

        self.entry.end_publication = datetime(2000, 3, 15)
        self.assertFalse(self.entry.is_actual)

    def test_is_visible(self):
        self.assertFalse(self.entry.is_visible)

        self.entry.status = PUBLISHED
        self.assertTrue(self.entry.is_visible)

        self.entry.start_publication = datetime(2020, 3, 15)
        self.assertFalse(self.entry.is_visible)

    def test_save_last_update(self):
        last_update = self.entry.last_update
        self.entry.save()
        self.assertNotEqual(
            last_update,
            self.entry.last_update)


class EntryHtmlContentTestCase(TestCase):

    def setUp(self):
        params = {
            'title': 'My entry',
            'content': 'My content'
        }
        self.entry = Entry(**params)

    def test_str(self):
        self.assertEqual(str(self.entry.html_preview), 'My content')

    def test_preview(self):
        large_content = (
            '<p>Lorem ipsum dolor sit amet, consectetur '
            'adipisicing elit<!--more-->. Porro repudiandae sapiente '
            'eaque velit earum deleniti impedit accusamus, '
            'corporis quia sit ex necessitatibus adipisci '
            'totam. Est non saepe harum aliquid quia, '
            'explicabo officiis ex quas! Eos doloremque '
            'quis ut eaque quos omnis quam, nihil, harum '
            'ex, assumenda eveniet. Recusandae eaque '
            'officiis quis nobis, quae aliquam tempora '
            'molestiae. Animi velit beatae eaque.</p>'
        )

        self.entry.content = large_content

        preview = (
            '<p>Lorem ipsum dolor sit amet, consectetur '
            'adipisicing elit ...</p>'
        )
        print(self.entry.html_preview)
        self.assertEqual(str(self.entry.html_preview), preview)
