from django.conf.urls import include, url
from django.contrib import admin

from products.views import (
    ProductCreateView,
    SellerProductListView,
    ProductUpdateView,
)
from .views import (
    SellerDashboard,
    SellerTransactionListView,
    SellerProductRedirectView
)

urlpatterns = [
    url(r'^$', SellerDashboard.as_view(), name='dashboard'),
    url(r'^transactions/$', SellerTransactionListView.as_view(), name='transactions'),
    url(r'^products/$', SellerProductListView.as_view(), name='product_list'), #sellers: product_list
    url(r'^products/add/$', ProductCreateView.as_view(), name='product_create'),
    url(r'^products/(?P<pk>\d+)/edit$', ProductUpdateView.as_view(), name='product_edit'),
    url(r'^products/(?P<pk>\d+)/$', SellerProductRedirectView.as_view(), name='product_edit'),
]
