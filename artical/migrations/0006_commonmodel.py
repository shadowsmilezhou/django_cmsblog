# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-10-26 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontAuth', '0001_initial'),
        ('artical', '0005_auto_20171018_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('creat_time', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artical.ArticalModel')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontAuth.FrontUserModel')),
            ],
        ),
    ]
