# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0002_auto_20160620_0431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='id',
        ),
        migrations.AlterField(
            model_name='word',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]