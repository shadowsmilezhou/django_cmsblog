#coding:utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CmsUser(models.Model):
	avatar = models.URLField(max_length=100,blank=True)
	#创建一个和User表一对一的关系，只能这样创建
	user = models.OneToOneField(User)