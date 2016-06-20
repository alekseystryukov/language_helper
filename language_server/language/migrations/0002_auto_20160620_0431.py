# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 04:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_of_speech_id', models.SmallIntegerField(blank=True, null=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='word',
            name='part_of_speech_id',
        ),
        migrations.RemoveField(
            model_name='word',
            name='participle_form',
        ),
        migrations.RemoveField(
            model_name='word',
            name='past_form',
        ),
        migrations.RemoveField(
            model_name='word',
            name='translation',
        ),
        migrations.AddField(
            model_name='meaning',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meanings', to='language.Word'),
        ),
    ]
