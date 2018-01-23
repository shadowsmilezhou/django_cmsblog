# -*- coding:utf-8 -*-
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,reverse,redirect
from cmsauth.models import CmsUser
from django.contrib.auth.models import User
from django.core.cache import cache
from forms import EditCategoryForm,CategoryForm,TopArticalForm,DeleteArticalForm ,LoginForm,UpdateProfileForm,UpdateEmailForm,AddCategoryForm,AddTagForm,AddArticalForm,UpdateArticalForm
from django.views.decorators.http import require_http_methods
from qiniu import Auth,put_file
from django.core import mail
import hashlib
import time
from artical.models import ArticalModel,CategoryModel,TagModel,TopModel
from utils import xtjson
from django.conf import settings
from django.forms import model_to_dict
from django.db.models import Count
def cms_login(request):
    if request.method == 'GET':
        return render(request,'cms_login.html')
    else:
        form = LoginForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            username = form.cleaned_data.get('username',None)
            password = form.cleaned_data.get('password',None)
            remember = form.cleaned_data.get('remember',None)
            print username,password
            #1.验证数据库里是否有这个用户
            user = authenticate(username=username,password=password)
            print 'user:',user
            if user:
                login(request,user)
                #1.判断
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                nexturl = request.GET.get('next')
                if nexturl:
                    return redirect(nexturl)
                else:
                    return redirect(reverse('cms_index'))#重定向到首页
                #reverse作用的是urls里面的name
            else:
                return render(request,'cms_login.html',{'error':u'用户名或者密码错误'})
        else:
            return render(request,'cms_login.html',{'error':form.get_error()})

def cms_logout(request):
    logout(request)
    return redirect(reverse('cms_login'))






def test(request):

    return HttpResponse('success')



def cms_settings(request):
    return render(request,'cms_settings.html')

@login_required
def update_profile(request):
    form = UpdateProfileForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username',None)
        avatar = form.cleaned_data.get('avatar',None)
        user = request.user
        #user = User.objects.all().first()
        user.username = username
        user.save()

        cmsuser = CmsUser.objects.filter(user__pk=user.pk).first()

        if not cmsuser:
            cmsuser = CmsUser(avatar=avatar,user=user) 
        else:
            cmsuser.avatar = avatar

        cmsuser.save()
        return xtjson.json_result()
    else:
        return xtjson.json_result(message=form.get_error())

@require_http_methods(['GET'])
def get_token(request):
    #1.获取ak，sk
    access_key = 'nzuhujy9DebvGiA5-cz4RGbW7iMBo1bQfnkoJ-N6'
    secret_key = '8fNUA0JhLU6MP-_vMYBUyfS85UaQf34AfUVS_b74'
    #2.授权
    q = Auth(access_key,secret_key)
    #3.设置七牛空间
    bucket_name = 'xtblogs'
    #4.生成七牛空间
    token = q.upload_token(bucket_name)

    return JsonResponse({'uptoken':token})

@login_required
@require_http_methods(['GET'])
def email_success(request):
    return render(request,'cms_emailsuccess.html')

@login_required
@require_http_methods(['GET'])
def email_fail(request):
    return render(request,'cms_emailfail.html')



@login_required
@require_http_methods(['GET','POST'])
def update_email(request):
    if request.method == 'GET':
        return render(request,'cms_email.html')
    else:
        form = UpdateEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email',None)
            if email:
                code = hashlib.md5(str(time.time())+email).hexdigest()
                #把用户的邮箱信息存储到缓存中
                #发送链接到email这个邮箱，用户点击了才算认证通过
                cache.set(code,email,120)
                check_url = request.scheme + '://' + request.get_host() + reverse('cms_check_email',kwargs={'code':code})
                subject = u'邮箱修改验证'
                message = u'博客验证链接，点击' + check_url +  u'  ,请在10分钟内完成注册。工作人员不会向您索取验证码，请勿泄露。消息来自：SmileSugar的博客'
                from_mail = '630551760@qq.com'
                recipient_list = [email]
                
                print 'check_url:',check_url
                # print 'scheme:',request.scheme
                # print 'host:',request.get_host()
                # print 'url',reverse('cms_check_email')
                if mail.send_mail(subject,message,from_mail,recipient_list):
                    return redirect(reverse('cms_email_success'))
                else:
                    return redirect(reverse('cms_email_fail'))
                
                #通过验证才能保存
                
        else:
            return render(request,'cms_email.html',{'error':form.get_error()})


@login_required
@require_http_methods(['GET'])
def check_email(request,code):
    if len(code) > 0:
        email = cache.get(code)
        if email:
            user = request.user
            user.email = email
            #update_fields这个可以参数可以指定需要保存哪些字段
            user.save(update_fields=['email'])
            return HttpResponse(u'邮箱修改成功')
        else:
            return HttpResponse(u'该链接已经失效')
            
    else:
        return HttpResponse(u'该链接已经失效')
    '''
    验证邮箱的url
    '''
    # 需要知道用户之前修改邮箱的时候填的是什么邮箱

#文章相关操作
@login_required  #如果登陆成功
def artical_manage(request,page=1,category_id=0):
    categoryId = int(category_id)
    if categoryId > 0:
        articals = ArticalModel.objects.all().filter(category__pk=categoryId).order_by('-top__opreate_time','-release_time')
    else:
        articals = ArticalModel.objects.all().order_by('-top__opreate_time','-release_time') 
    currentPage = int(page)
    numPage = int(settings.NUM_PAGE) #一页加载的文章数量
    start = (currentPage-1)*15
    end = start + 15
    articalsCount = articals.count()
    articals = articals[start:end]

    pageCount = articalsCount/numPage
    if articalsCount%numPage > 0:
        pageCount += 1

    pages = []

    tmpPage = currentPage-1
    while tmpPage >= 1:
        if tmpPage % 5 == 0:
            break
        else:
            pages.append(tmpPage)
            tmpPage -= 1

    tmpPage = currentPage
    while tmpPage <= pageCount:
        if tmpPage % 5 == 0:
            pages.append(tmpPage)
            break
        else:
            pages.append(tmpPage)
            tmpPage += 1

    pages.sort()

    categorys = CategoryModel.objects.all()
    context = {
        'c_page':currentPage,
        'pages':pages,
        't_page':pageCount,
        'articals':articals,
        'categorys':categorys,
        'c_category':categoryId,
    }
    return render(request,'cms_artical_manage.html',context=context)


@login_required
@require_http_methods(['POST','GET'])
def edit_artical(request,pk=''):
    if request.method == 'GET':
        artical = ArticalModel.objects.filter(pk=pk).first()
        Artical = ArticalModel.objects.filter(pk=pk).first()
        print artical.uid
        # print artical.tags.all()
        articalDict = model_to_dict(artical)
        articalDict['tags'] = []
        for tagModel in artical.tags.all():
            articalDict['tags'].append(tagModel.id)

        print articalDict
        context = {
            'Artical':Artical,
            'artical': articalDict,
            'categorys': CategoryModel.objects.all(),
            'tags':TagModel.objects.all()
        }
        return render(request,'cms_edit_artical.html',context)
    else:
        form = UpdateArticalForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content_html = form.cleaned_data.get('content_html')
            tags = request.POST.getlist('tags[]')
            print tags
            uid = form.cleaned_data.get('uid')
            articalModel = ArticalModel.objects.filter(pk=uid).first()
            if articalModel:
                articalModel.title = title
                articalModel.desc = desc
                articalModel.thumbnail = thumbnail
                articalModel.content_html = content_html
                articalModel.category = CategoryModel.objects.filter(pk=category).first()
                articalModel.save()

                if tags:
                    for tag in tags:
                        tagModel = TagModel.objects.filter(pk=tag).first()
                        articalModel.tags.add(tagModel)
                        articalModel.save()
            return xtjson.json_result()
        else:
            return form.get_error_response()


@login_required
def add_artical(request):
    if request.method == 'GET':
        categorys = CategoryModel.objects.all()
        tags = TagModel.objects.all()
        data = {
        'categorys':categorys,
        'tags':tags
        }
        return render(request,'cms_artical.html',data)
    else:
        form = AddArticalForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content_html = form.cleaned_data.get('content_html')
            tags = request.POST.getlist('tags[]')
            user = request.user
            categoryModel = CategoryModel.objects.filter(pk=category).first()
            articalModel =  ArticalModel(title=title,desc=desc,thumbnail=thumbnail,content_html=content_html,author=user,category=categoryModel)
            articalModel.save()
            for tag in tags:
                tagModel = TagModel.objects.filter(pk=int(tag)).first()
                if tagModel:
                    articalModel.tags.add(tagModel)
            return xtjson.json_result()
        else:
            return form.get_error_response()
        # return HttpResponse('xxx')

@login_required
@require_http_methods(['POST'])
def delete_artical(request):
    form = DeleteArticalForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articalModel = ArticalModel.objects.filter(pk=uid).first()
        if articalModel:
            articalModel.delete()
            return xtjson.json_result() 
        else:
            return xtjson.json_params_error(message=u'该博客不存在')
    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def top_artical(request):
    form = TopArticalForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articalModel = ArticalModel.objects.filter(pk=uid).first()
        if articalModel:
            if articalModel.thumbnail:
                topModel = articalModel.top
            else:
                return xtjson.json_params_error('置顶文章需要缩略图')
            
            if not topModel:
                topModel = TopModel()
            topModel.save()

            articalModel.top = topModel
            articalModel.save(update_fields=['top'])
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message=u'该博客不存在')
    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def untop_artical(request):
    form = TopArticalForm(request.POST)
    if form.is_valid():
        uid = form.cleaned_data.get('uid')
        articalModel = ArticalModel.objects.filter(pk=uid).first()
        if articalModel:
            if articalModel.top:
                topModel = articalModel.top
                topModel.delete()
                return xtjson.json_result()
            else:
                return xtjson.json_params_error(message=u'该文章未置顶')
        else:
            return xtjson.json_params_error(message=u'该文章不存在')
    else:
        return form.get_error_response()

@login_required
@require_http_methods(['GET'])
def category_manage(request):
    if request.method == 'GET':
        categorys = CategoryModel.objects.all().annotate(num_articals=Count('articalmodel')).order_by('-num_articals')
        context = {
        'categorys':categorys
        }   
        return render(request,'cms_category_manage.html',context=context) 

@login_required
@require_http_methods(['POST'])
def edit_category(request):
    form = EditCategoryForm(request.POST)
    if form.is_valid():
        categoryId = form.cleaned_data.get('category_id')
        name = form.cleaned_data.get('name')
        categoryModel = CategoryModel.objects.all().filter(pk=categoryId).first()
        if categoryModel:
            categoryModel.name = name
            categoryModel.save(update_fields=['name'])
            return xtjson.json_result()
        else:
            return xtjson.json_params_error(message='该分类不存在') 
    else:
        return form.get_error_response()

@login_required
@require_http_methods(['POST'])
def delete_category(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        categoryId = form.cleaned_data.get('category_id')
        categoryModel = CategoryModel.objects.all().filter(pk=categoryId).first()
        if categoryModel:
            articalCount = categoryModel.articalmodel_set.all().count()
            if articalCount > 0:
                return xtjson.json_params_error(message='无法删除，该分类下还有文章')
            else:
                categoryModel.delete()
                return xtjson.json_result()

    else:
        return form.get_error_response()


@login_required
@require_http_methods(['POST'])
def add_category(request):
    form = AddCategoryForm(request.POST)
    print form.is_valid()
    if form.is_valid():
        categoryname = form.cleaned_data.get('categoryname',None)
        oldCategoryname = CategoryModel.objects.filter(name=categoryname).first()
        if not oldCategoryname:
            categoryname = CategoryModel(name=categoryname)
            categoryname.save()
            print categoryname.id,categoryname.name
         #   return JsonResponse({'code':200,'data':{'id':categoryname.id,'name':categoryname.name}})
            return xtjson.json_result(data={'id':categoryname.id,'name':categoryname.name})
        else:
            # return JsonResponse({'code':u'名字不能重复','code':403})
            return xtjson.json_params_error(message=u'名字不能重复')
    else:   
        return xtjson.json_params_error(message=u'表单验证失败') 

@login_required
@require_http_methods(['POST'])
def add_tags(request):
    form = AddTagForm(request.POST)
    if form.is_valid():
        tagname = form.cleaned_data.get('tagname')
        resultTag = TagModel.objects.filter(name=tagname).first()
        if not resultTag:
            tagModel = TagModel(name=tagname)
            tagModel.save()
            return xtjson.json_result(data={'id':tagModel.id,'name':tagModel.name})
        else:
            return xtjson.json_params_error(message=u'名字不能重复')

    else:
        return form.get_error_response()


def test(request):
    for x in xrange(0,100):
        title = u'博客标题%s' % x
        category = CategoryModel.objects.all().first()
        content_html = u'博客内容%s' % x
        articalModel = ArticalModel(title=title,content_html=content_html,category=category)
        articalModel.save()
    return xtjson.json_result()
