# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0009_auto_20171122_0529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(default='img/default.png', upload_to='img/%Y/%m/'),
        ),
    ]