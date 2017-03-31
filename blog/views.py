from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from blog.models import Entry

# Create your views here.
class EntryList(ListView):
    model = Entry
    template_name = 'blog/entry_list.html'
    context_object_name = 'entries'
    page_kwarg = 'page'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        return super(EntryList, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Entry.published.all()


class EntryDetail(DetailView):
    model = Entry
    template_name = 'blog/entry_detail.html'
    context_object_name = 'entry'
    pk_url_kwarg = 'entry_id'