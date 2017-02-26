# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-17 03:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dndb', '0003_auto_20170210_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dndb.Campaign')),
                ('giver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dndb.Character')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dndb.Location')),
            ],
        ),
    ]