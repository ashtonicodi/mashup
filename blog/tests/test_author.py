from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.managers import PUBLISHED
from blog.models import Author
from blog.models import Entry


class AuthorTestCase(TestCase):

    def setUp(self):
        self.author = Author.objects.create_user(
            'webmaster', 'webmaster@example.com')
        params = {
            'title': 'My entry',
            'content': 'My content',
        }

        self.entry = Entry.objects.create(**params)
        self.entry.authors.add(self.author)

    def test_entries_published(self):
        self.assertEqual(self.author.entries_published().count(), 0)
        self.entry.status = PUBLISHED
        self.entry.save()
        self.assertEqual(self.author.entries_published().count(), 1)

    def test_str(self):
        self.assertEqual(self.author.__str__(),
                         'webmaster')
        self.author.first_name = 'John'
        self.assertEqual(self.author.__str__(),
                         'John')
        self.author.last_name = 'Doe'
        self.assertEqual(self.author.__str__(),
                         'John Doe')

    def test_manager_pollution(self):
        """
        https://github.com/Fantomas42/django-blog-zinnia/pull/307
        """
        self.assertNotEqual(get_user_model().objects.model,
                            Author)