from django.test import TestCase

from blog.managers import PUBLISHED
from blog.models import Category
from blog.models import Entry


class CategoryTestCase(TestCase):

    def setUp(self):
        self.categories = [Category.objects.create(title='Category 1',
                                                   slug='category-1'),
                           Category.objects.create(title='Category 2',
                                                   slug='category-2')]
        params = {
            'title': 'My entry',
            'content': 'My content',
        }

        self.entry = Entry.objects.create(**params)
        self.entry.categories.add(*self.categories)

    def test_entries_published(self):
        category = self.categories[0]
        self.assertEqual(category.entries_published().count(), 0)
        self.entry.status = PUBLISHED
        self.entry.save()
        self.assertEqual(category.entries_published().count(), 1)

        params = {'title': 'My second entry',
                  'content': 'My second content',
                  'status': PUBLISHED,}

        new_entry = Entry.objects.create(**params)
        new_entry.categories.add(self.categories[0])

        self.assertEqual(self.categories[0].entries_published().count(), 2)
        self.assertEqual(self.categories[1].entries_published().count(), 1)