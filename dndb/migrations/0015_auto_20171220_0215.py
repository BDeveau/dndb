# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-12-20 02:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dndb', '0014_auto_20170512_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
