#coding:utf8

from django.http import JsonResponse
from collections import namedtuple

"""
http 状态码
200:请求正常
400：请求参数错误
401：没有权限访问
405：方法不允许，请求方法错误
"""
HttpCode = namedtuple('HttpCode',['ok','paramserror','unauth','methoderror'])
httpcode = HttpCode(ok=200,paramserror=400,unauth=401,methoderror=405)

def json_result(code=httpcode.ok,message='',data={},kwargs={}):
	json = {'code':code,'message':message,'data':data}
	for k,v in kwargs.items():
		json['k'] = v
	return JsonResponse(json)

def json_params_error(message=''):
	return json_result(code=httpcode.paramserror,message=message)

def json_unauth_error(message=''):
	return json_result(code=httpcode.unauth,message=message)

def json_method_error(message=''):
	return json_result(code=httpcode.methoderror,message=message)