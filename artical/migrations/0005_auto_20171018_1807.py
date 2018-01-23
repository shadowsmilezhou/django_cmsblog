# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-18 10:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artical', '0004_articalmodel_read_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opreate_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='articalmodel',
            name='top',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='artical.TopModel'),
        ),
    ]
