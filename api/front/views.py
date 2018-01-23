# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render,redirect,reverse
from artical.models import ArticalModel,CategoryModel,CommentModel
from utils import xtjson
from django.forms import model_to_dict
from django.views.decorators.http import require_http_methods
from forms import CommentForm,ResetpwdForm,SignupForm,SigninForm,ForgetpwdForm
from utils.xtemail import send_email
from django.core.cache import cache
from frontAuth.models import FrontUserModel
from frontAuth.utlis import login,logout
from frontAuth.decorators import front_login_required
from django.conf import settings
from django.db.models import Q
def artical_list(request,category_id=0,page=1):
	categoryId = int(category_id)
	currentPage = int(page)
	numPage = int(settings.NUM_PAGE)

	start = (currentPage-1)*numPage
	end = start + numPage

	articals = ArticalModel.objects.all()

	topArtical = None

	if categoryId > 0 :
		articals = articals.filter(category_id=categoryId)
	else:
		topArtical = articals.filter(top__isnull=False).order_by('-top__opreate_time')
		articals = articals.filter(top__isnull=True).order_by('-update_time')

	articals = list(articals.values()[start:end])

	context = {
		'articals':articals,
		'c_page':currentPage,
	}

	if request.is_ajax():
		return xtjson.json_result(data=context)
	else:
		context['categorys'] = CategoryModel.objects.all()
		context['top_articals'] = topArtical
		context['c_category'] = CategoryModel.objects.filter(pk=category_id).first()
		return render(request,'front_artical_list.html',context=context)
	
def artical_detail(request,artical_id=''):
	articalId = artical_id
	if articalId:
		articalModel = ArticalModel.objects.filter(pk=articalId).first()
		if articalModel:
			comments = articalModel.commentmodel_set.all()
			context = {
				'categorys':CategoryModel.objects.all(),
				'artical': articalModel,
				'c_category':articalModel.category,
				'tags':articalModel.tags.all(),
				'comments':comments
			}
			return render(request,'front_artical_detail.html',context)
		else:
			return xtjson.json_params_error(message='该文章不存在')
		
	else:
		return xtjson.json_params_error(message='文章id不能为空')

@require_http_methods(['POST','GET'])
def signin(request):
	if request.method == 'GET':
		return render(request,'front_signin.html')
	else:
		form = SigninForm(request.POST)
		print form.is_valid()
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = login(request,email,password)
			if user:
				remember = form.cleaned_data.get('remember')
				if remember:
					request.session.set_expiry(None)
				else:
					request.session.set_expiry(0)
				nexturl = request.GET.get('next')
				print nexturl
				if nexturl:
					return redirect(nexturl)
				else:
					return redirect(reverse('front_index'))
			else:
				return render(request,'front_signin.html',{'error':u'用户名和密码错误'})
		else:
			return render(request,'front_signin.html',{'error':form.get_error()})


@require_http_methods(['POST','GET'])
def signup(request):
	if request.method == 'GET':
		return render(request,'front_signup.html')
	else:
		form = SignupForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			cache_data = {
				'email':email,
				'username':username,
				'password':password
			}
			if send_email(request,email,'front_check_email',cache_data):
				return HttpResponse(u'邮件发送成功')
			else:
				return HttpResponse(u'邮件发送失败')
		else:
			return xtjson.json_params_error(message=form.get_error())

def signout(request):
	logout(request)
	return redirect(reverse('front_index'))


def check_email(request,code=''):
	cache_data = cache.get(code)
	email = cache_data.get('email')
	username = cache_data.get('username')
	password = cache_data.get('password')

	user = FrontUserModel(email=email,username=username,password=password)
	user.save()

	return redirect(reverse('front_signin'))

@require_http_methods(['POST','GET'])
def forget_password(request):
	if request.method == 'GET':
		return render(request,'front_forgetpwd.html')
	else:
		form = ForgetpwdForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			user = FrontUserModel.objects.filter(email=email).first()
			if user:
				if send_email(request,email,'front_reset_password'):
					return HttpResponse(u'邮件发送成功')
				else:
					return HttpResponse(u'邮件发送失败')

			else:
				return HttpResponse(u'邮件不存在')
		else:
			return render(request,'front_forgetpwd.html',{'error':form.get_error()})


def reset_password(request,code=''):
	if request.method == 'GET':
		return render(request,'front_resetpwd.html')
	else:
		form = ResetpwdForm(request.POST)
		if form.is_valid():
			print code
			email = cache.get(code)
			print email
			password = form.cleaned_data.get('password')
			user = FrontUserModel.objects.filter(email=email).first()
			if user:
				user.set_password(password)
				return HttpResponse(u'密码修改成功')
			else:
				return HttpResponse(u'没有该用户')

		else:
			return render(request,'front_resetpwd.html',{'error':form.get_error()})

@require_http_methods(['POST'])
@front_login_required
def comment(request):
	form = CommentForm(request.POST)
	if form.is_valid():
		content = form.cleaned_data.get('content')
		articalId =  form.cleaned_data.get('artical_id')
		articalModel = ArticalModel.objects.filter(pk=articalId).first()
		print articalModel
		if articalModel:
			commentModel = CommentModel(content=content,artical=articalModel,author=request.front_user)
			commentModel.save()
			return redirect(reverse('front_artical_detail',kwargs={'code':articalId}))
			# return xtjson.json_result()
	else:
		return xtjson.json_params_error(message=form.get_error())


@require_http_methods(['GET'])
def search(request):
	q = request.GET.get('query')

	if q:
		articals = ArticalModel.objects.filter(Q(title__icontains=q)|Q(content_html__icontains=q))
		context = {
		'articals':articals,
		'categorys':CategoryModel.objects.all()
		}
		return render(request,'front_search.html',context)

	else:
		return xtjson.json_params_error(message=u'请输入查询字符串')