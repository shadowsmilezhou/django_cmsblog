# -*- coding:utf-8 -*-

from django import forms
from utils.captcha.xtcaptcha import Captcha
import json
from utils import xtjson
class BaseForm(forms.Form):
    def get_error(self):
        errors = self.errors.as_json()
        errors_dict = json.loads(errors)
        message = ''
        print errors_dict
        for k,v in errors_dict.items():
            message = v[0].get('message',None)
        return message

    def get_error_response(self):
        if self.errors:
            return xtjson.json_params_error(message=self.get_error())
        else:
            return xtjson.json_result()

class LoginForm(BaseForm):
    username = forms.CharField(max_length=10,min_length=4)
    password = forms.CharField(max_length=20,min_length=6)
    captcha = forms.CharField(max_length=4,min_length=4)
    remember = forms.BooleanField(required=False)#用户可能不需要记住我，这个参数就没有
    #是布尔类型
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha',None)
        if not Captcha.check_captcha(captcha):
           raise forms.ValidationError(u'验证码错误!')
        return captcha

   

class  UpdateProfileForm(BaseForm):
    username = forms.CharField(max_length=10,min_length=4)
    avatar = forms.URLField(max_length=100,required=False)


class UpdateEmailForm(BaseForm):
    email = forms.EmailField(required=True)

class AddCategoryForm(BaseForm):
    categoryname = forms.CharField(max_length=20)


class AddTagForm(BaseForm):
    tagname = forms.CharField(max_length=20)

class AddArticalForm(BaseForm):
    title = forms.CharField(max_length=200)
    category = forms.IntegerField(required=True)
    desc = forms.CharField(max_length=200,required=False)
    thumbnail = forms.URLField(max_length=100,required=False)
    content_html = forms.CharField()

class UpdateArticalForm(AddArticalForm):
    uid = forms.UUIDField()

class DeleteArticalForm(BaseForm):
    uid = forms.UUIDField()

class TopArticalForm(BaseForm):
    uid = forms.UUIDField(error_messages={'required=':u'文章ID不能少'})

class CategoryForm(BaseForm):
    category_id = forms.IntegerField()

class EditCategoryForm(CategoryForm):
    name = forms.CharField()