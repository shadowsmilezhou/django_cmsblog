# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,reverse
from django.http import HttpResponse
from models import FrontUserModel
from utlis import login,logout
import configs
from decorators import front_login_required
# Create your views here.front_login_required
def add_user(request):
	user = FrontUserModel(email='aaa@qq.com',username='aaa',password='aaa')
	user.save()
	return HttpResponse('success~~~')

def test1(request):
	email = 'aaa@qq.com'
	password = 'aaa1'
	user = FrontUserModel.objects.filter(email=email).first()
	user.set_password('aaaaaa')
	# if user.check_password(password):
	# 	return HttpResponse('You are Right')
	# else:
	# 	return HttpResponse('You are Wrong')
	return HttpResponse('success')

def front_login(request):
	email = 'aaa@qq.com'
	password = 'bbb'

	user = login(request,email,password)

	if user:
		return HttpResponse(u'登录成功')
	else:
		return HttpResponse(u'登录失败')

def check_login(request):
	uid = request.session.get(configs.LOGINED_KEY)
	user = FrontUserModel.objects.filter(pk=uid).first()
	if user:
		return HttpResponse('success')
	else:
		return HttpResponse('failed')



def front_logout(request):
	logout(request)
	return HttpResponse(u'退出成功')

@front_login_required
def decorator_check(request):
	print '-'*30
	print reverse('front_signin') + '?next=' + request.path
	print '-'*30
	return HttpResponse(u'您在已经登录的情况下访问改页面')


def middleware_test(request):
	if not hasattr(request,'front_user'):
		return HttpResponse(u'失败')
	else:
		return HttpResponse(u'成功')




