# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-17 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artical', '0002_auto_20171016_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='articalmodel',
            name='release_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='articalmodel',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
