# -*- coding:utf-8 -*-

from django import forms
from api.common.forms import BaseForm
from django.core.cache import cache
from utils.captcha.xtcaptcha import Captcha

class CaptchaForm(forms.Form):
	captcha = forms.CharField(max_length=4,min_length=4)

	def clean_captcha(self):
		captcha = self.cleaned_data.get('captcha')
		if not Captcha.check_captcha(captcha):
			raise forms.validationError(u'验证码错误')

		return captcha

class SignupForm(BaseForm,CaptchaForm):
	email = forms.EmailField()
	username = forms.CharField(max_length=20,min_length=4)
	password = forms.CharField(max_length=20,min_length=6)
	captcha = forms.CharField(max_length=4,min_length=4)




class SigninForm(BaseForm):
	email = forms.EmailField()
	password = forms.CharField(max_length=20,min_length=6)
	remember = forms.BooleanField(required=False)

class ForgetpwdForm(BaseForm,CaptchaForm):
	email = forms.EmailField()


class ResetpwdForm(BaseForm):
	password = forms.CharField(max_length=20)
	password_repeat = forms.CharField(max_length=20)

	def clean(self):
		password = self.cleaned_data.get('password')
		password_repeat = self.cleaned_data.get('password_repeat')

		if password != password_repeat:
			raise forms.ValidationError(u'两次密码输入不一致')

		return self.cleaned_data

class CommentForm(BaseForm):
	content = forms.CharField(max_length=2000)
	artical_id = forms.CharField()