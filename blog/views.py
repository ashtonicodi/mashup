from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from mashup.blog.models import Entry

# Create your views here.
class EntryList(ListView):
    model = Entry
    template_name = 'blog/entry_list.html'
    context_object_name = 'entries'
    page_kwarg = 'page'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        pass

    def get_queryset(self):
        pass


class EntryDetail(DetailView):
    model = Entry
    template_name = 'blog/entry_detail.html'
    context_object_name = 'entry'