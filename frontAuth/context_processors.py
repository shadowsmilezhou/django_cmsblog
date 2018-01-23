#coding:utf-8
import configs
from models import FrontUserModel

def auth(request):
	'''
	1.首先判断当前用户是否已经登录，登录了才有front_user变量
	2.如果当前已经登录了，并且request已经有了该属性，直接拿来用
	3.如果当前已经登录，但是没有那就添加上去
	'''
	if request.session.get(configs.LOGINED_KEY):
		if hasattr(request,'front_user'):
			print request.front_user.username
			return {'front_user':request.front_user}
		else:
			uid = request.session.get(configs.LOGINED_KEY)
			user = FrontUserModel.objects.filter(pk=uid).first()
			return {'front_user':user}
	else:
		return {}
