# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-03 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dndb', '0007_auto_20170223_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed',
            field=models.NullBooleanField(),
        ),
    ]