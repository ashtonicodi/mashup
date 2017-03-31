from django.conf.urls import url

from blog.views import EntryList, EntryDetail

urlpatterns = [
    url(r'^$', EntryList.as_view(), name='entry_list'),
    url(r'^(?P<page>[0-9]+)$', EntryList.as_view(), name='entry_list'),
    url(r'^post/(?P<entry_id>[0-9]+)$', EntryDetail.as_view(), name='entry_detail')
]
