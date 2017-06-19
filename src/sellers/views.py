# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.views.generic import View
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from digitalmarket.mixins import LoginRequiredMixin

from billing.models import Transaction
from products.models import Product

from .forms import NewSellerForm
from .mixins import SellerAccountMixin
from .models import SellerAccount

class SellerTransactionListView(ListView):
    model = Transaction
    template_name = "sellers/transaction_list_view.html"

    def get_queryset(self):
        return self.get_transaction()
        # account = SellerAccount.objects.filter(user=self.request.user)
        # if account.exists():
        #     products = Product.objects.filter(seller=account)
        #     return Transaction.objects.filter(product__in=products)
        # return []


class SellerDashboard(SellerAccountMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = "/seller/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        apply_form = self.get_form() #NewSellerForm
        account = self.get_account()
        exists = account
        active = None
        context = {}

        if exists:
            active = account.active
        #if no exists, show form
        #if exists and no active , show pending
        #if exists and active, show dashboard data
        if not exists and not active:
            context["title"] = "Aplly for Account"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account pending"
        elif exists and active:
            context["title"] = "Seller Dashboard"
            # products = Product.objects.filter(seller=account)
            context["products"] = self.get_products()
            context["transactions"] = self.get_transaction()[:5]
        else:
            pass

        return render(request , "sellers/dashboard.html", context)

    def form_valid(self,form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data
