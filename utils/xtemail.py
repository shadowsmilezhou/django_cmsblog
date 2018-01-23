#coding:utf-8

import hashlib
from django.core.cache import cache
from django.shortcuts import reverse
from django.conf import settings
import time
from django.core import mail


def send_email(request,email,check_url,cache_data=None,message=None,subject=None):
	code = hashlib.md5(str(time.time()) + email).hexdigest()
	if cache_data:
		cache.set(code,cache_data,120)
	else:
		cache.set(code,email,120)

	url = request.scheme+'://' + request.get_host() + reverse(check_url,kwargs={'code':code})

	if not subject:
		subject = u'邮箱验证'

	if not message:
		message = u'博客验证链接，点击 ' + url + u'  ,请在10分钟内完成注册。工作人员不会向您索取验证码，请勿泄露。消息来自：SmileSugar的博客'

	from_mail = settings.EMAIL_HOST_USER
	recipient_list = [email]
	if mail.send_mail(subject,message,from_mail,recipient_list):
		return True
	else:
		return False

