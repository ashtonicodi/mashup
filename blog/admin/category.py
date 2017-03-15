from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from blog.admin.forms import CategoryAdminForm


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for Category model.
    """
    form = CategoryAdminForm
    fields = ('title', 'description', 'slug')
    list_display = ('id', 'title', 'slug', 'description')
    list_display_links = ('id', 'title', 'slug')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'description')