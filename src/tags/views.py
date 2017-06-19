# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from analytics.models import TagView
from .models import Tag

class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, *args, **kwargs):
        context = super(TagDetailView, self).get_context_data(*args, **kwargs)
        print context
        print self.get_object().products.count()
        if self.request.user.is_authenticated():
            tag = self.get_object()
            new_view = TagView.objects.add_count(self.request.user, tag)
        return context


class TagListView(ListView):
    model = Tag

    def get_queryset(self):
        return Tag.objects.all()
