# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 04:19
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20170608_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location=b'/Users/bach/Desktop/python/myvirtualenv/digitalmarket/static_cdn/protected'), upload_to=products.models.download_media_location),
        ),
    ]