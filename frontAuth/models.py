# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
import hashers
# Create your models here.

class FrontUserModel(models.Model):
	"""docstring for Front"""
	uid = models.UUIDField(primary_key=True,default=uuid.uuid4)
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=128)
	avatar = models.URLField(blank=True)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(auto_now_add=True)

	def __init__(self,*args,**kwargs):
		if 'password' in kwargs:
			hash_password = hashers.make_password(kwargs['password'])
			kwargs['password'] = hash_password
		super(FrontUserModel,self).__init__(*args,**kwargs)

	def check_password(self,raw_password):
		return hashers.check_password(raw_password,self.password)


	#修改密码
	def set_password(self,raw_password):
		if not raw_password:
			return None

		hash_password = hashers.make_password(raw_password)
		self.password = hash_password
		self.save(update_fields=['password'])


	