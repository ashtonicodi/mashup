from django import forms

from blog.models import Category


class CategoryAdminForm(forms.ModelForm):
    '''
    form for Category's admin.
    '''
    class Meta:
        '''
        CategoryAdminForm's meta.
        '''
        model = Category
        fields = forms.ALL_FIELDS