# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from mimetypes import guess_type

from django.conf import settings
from wsgiref.util import FileWrapper
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from analytics.models import TagView
from digitalmarket.mixins import (
        MultiSlugMixin,
        SubmitBtnMixin,
        LoginRequiredMixin,
        StaffRequiredMixin
    )
from sellers.mixins import SellerAccountMixin
from tags.models import Tag

from .forms import ProductAddForm, ProductModelForm
from .mixins import ProductManagerMixin
from .models import Product

class ProductCreateView(SellerAccountMixin, LoginRequiredMixin, SubmitBtnMixin, CreateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    # success_url = "/products/"
    submit_btn = "Add Product"

    def form_valid(self,form):
        seller = self.get_account()
        form.instance.seller = seller
        valid_data = super(ProductCreateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        if tags:
            tags_list = tags.split(",")
            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(form.instance)
        return valid_data

    # def get_success_url(self):
    #     return reverse("products:list")

class ProductUpdateView(SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = Product
    template_name = "form.html"
    form_class = ProductModelForm
    # success_url = "/products/"
    submit_btn = "Update Product"

    def get_initial(self):
        initial = super(ProductUpdateView,self).get_initial()
        print initial
        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        """
            tag_list = []
            for x in tags:
                tag_list.append(x.title)
        """
        return initial

    def form_valid(self, form):
        valid_data = super(ProductUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tags_list = tags.split(",")
            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(self.get_object())
        return valid_data

class ProductDetailView(MultiSlugMixin, DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        for tag in tags:
            new_view = TagView.objects.add_count(self.request.user, tag)

        return context

class ProductDownloadView(MultiSlugMixin, DetailView):
    model = Product

    def get(self, request ,*args, **kwargs):
        obj = self.get_object()
        if obj in request.user.myproducts.products.all():
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(file(filepath))
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type
            response = HttpResponse(wrapper, content_type=mimetype)

            if not request.GET.get("preview"):
                response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)

            response["X-SendFile"] = str(obj.media.name)
            return response
        else:
            raise Http404

class SellerProductListView(ListView):
    model = Product
    # template_name = "sellers/prouduct_list_view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(SellerProductListView, self).get_queryset(**kwargs)
        qs = qs.filter(seller=self.get_account())
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(description__icontains=query)
                ).order_by("title")
        return qs

class ProductListView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(description__icontains=query)
                ).order_by("title")
        return qs

def create(request):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "form": form,
        "submit_btn": "Create Product"
        }
    return  render(request, template, context)


# @login_required
def update_view(request, object_id=None):
    product = get_object_or_404(Product , id=object_id)
    form = ProductModelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        # instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "object": product,
        "form": form,
        "submit_btn": "Update Product"
        }
    return render(request, template, context)

def detail_slug(request, slug=None):
    product = Product.objects.get(slug=slug)
    try:
        product = get_object_or_404(Product , slug=slug)
    except Product.MultipleObjectsReturned:
        product = Product.objects.filter(slug=slug).order_by("-title").first()
    # print slug
    # product = 1
    template = "detail_view.html"
    context = {
        "object": product
        }
    return render(request, template, context)

def detail(request, object_id=None):
    product = get_object_or_404(Product , id=object_id)
    template = "detail_view.html"
    context = {
        "object": product
        }
    return render(request, template, context)

def list(request):
    # list all item
    print request
    queryset = Product.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)