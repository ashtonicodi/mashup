from django.conf.urls import url

from mashup.blog.views import EntryList, EntryDetail

urlpatterns = [
    url(r'^$', EntryList.as_view(), name='entry_list'),
    url(r'^(?P<page>[0-9]+)$', EntryList.as_view(), name='entry_list')
]
