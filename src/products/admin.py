# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import (
    Product,
    MyProducts,
    Thumbnail,
    ProductRating,
    CuratedProducts
)

class ThumbnailInline(admin.TabularInline):
    extra = 1
    model = Thumbnail

class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]
    list_display = ["__unicode__", "description", "price", "sale_price"]
    search_fields = ["title","description"]
    list_filter = ["price"]
    list_editable = ["sale_price"]
    # prepopulated_fields = {"slug" :("title",)}
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

# admin.site.register(Thumbnail)

admin.site.register(MyProducts)

admin.site.register(Thumbnail)

admin.site.register(ProductRating)

admin.site.register(CuratedProducts)
