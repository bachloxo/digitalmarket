# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 12:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20170609_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thumbnail',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
