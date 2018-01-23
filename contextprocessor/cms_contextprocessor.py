#coding:utf8
from django.contrib.auth.models import User
from cmsauth.models import CmsUser
def CmsContextProcessor(request):
	user = request.user
	#给user添加一个avatar属性
	#avatar 存储在cmsUser里面
	#相当于把CmsUser的avatar属性添加到user中
	if not hasattr(user,'avatar'):
		cmsuser = CmsUser.objects.filter(user__pk=user.pk).first()
		if cmsuser:
			setattr(user,'avatar',cmsuser.avatar)

	return {'user':user}