# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 06:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 21, 6, 25, 42, 223571)),
        ),
        migrations.AlterField(
            model_name='video',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='video',
            name='searched',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
