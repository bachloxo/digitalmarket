# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

from products.models import Product
# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, blank=True) #100.0
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    success = models.BooleanField(default=True)
    # transaction_id_payment_system = Braintree / Stripe
    # payment_method
    # last_four

    def __unicode__ (self):
        return "%s" %(self.id)
