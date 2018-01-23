# -*- coding:utf-8 -*-

from django.conf.urls import url,include
import views

urlpatterns = [

    url(r'^$',views.artical_list,name='front_index'),
    url(r'^artical_list/(?P<category_id>\d+)/(?P<page>\d+)/$',views.artical_list,name='front_artical_list'),
    url(r'^artical_detail/(?P<artical_id>[\w\-]+)/$',views.artical_detail,name='front_artical_detail'),
    url(r'^signin/$',views.signin,name='front_signin'),
    url(r'^signup/$',views.signup,name='front_signup'),
    url(r'^check_email/(?P<code>\w+)/$',views.check_email,name='front_check_email'),
    url(r'^forget_password/$',views.forget_password,name='front_forget_password'),
    url(r'^reset_password/(?P<code>\w+)/$',views.reset_password,name='front_reset_password'),
    url(r'^comment/$',views.comment,name='front_comment'),
    url(r'^research/$',views.search,name='front_search'),
]
