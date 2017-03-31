from django.contrib import admin

from blog.admin.category import CategoryAdmin
from blog.models import Category, Entry

admin.site.register(Entry)
admin.site.register(Category, CategoryAdmin)