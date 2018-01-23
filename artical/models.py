#coding:utf-8
from __future__ import unicode_literals

from django.db import models
import uuid
from django.contrib.auth.models import User
from frontAuth.models import FrontUserModel

# Create your models here.
class ArticalModel(models.Model):
	uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	author = models.ForeignKey(User,null=True)
	title = models.CharField(max_length=100)
	category = models.ForeignKey('CategoryModel')
	desc = models.CharField(max_length=200)
	thumbnail = models.ImageField(blank=True)
	tags = models.ManyToManyField('TagModel',blank=True)
	content_html = models.TextField()
	release_time = models.DateTimeField(auto_now_add=True,null=True)
	update_time = models.DateTimeField(auto_now=True,null=True)
	read_count = models.IntegerField(default=0)
	top = models.ForeignKey('TopModel',null=True,on_delete=models.SET_NULL)

class TopModel(models.Model):
	opreate_time = models.DateTimeField(auto_now=True)

class CategoryModel(models.Model):
	name = models.CharField(max_length=20,unique=True)

class TagModel(models.Model):
	name = models.CharField(max_length=20,unique=True)

class CommentModel(models.Model):
	author = models.ForeignKey(FrontUserModel)
	content = models.TextField()
	creat_time = models.DateTimeField(auto_now_add=True)
	artical = models.ForeignKey(ArticalModel)