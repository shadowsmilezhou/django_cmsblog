# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-26 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artical', '0007_auto_20171026_2016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commentmodel',
            old_name='article',
            new_name='artical',
        ),
    ]