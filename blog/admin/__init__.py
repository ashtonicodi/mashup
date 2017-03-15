from django.contrib import admin

from blog.admin.category import CategoryAdmin
from blog.models import Category


admin.site.register(Category, CategoryAdmin)