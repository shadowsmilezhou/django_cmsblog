# -*- coding:utf-8 -*-
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.artical_manage, name='cms_index'),
    url(r'^login/$', views.cms_login, name='cms_login'),
    url(r'^logout/$', views.cms_logout, name='cms_logout'),
    url(r'^add_artical/$', views.add_artical, name='cms_add_artical'),
    url(r'^artical_manage/(?P<page>\d+)/(?P<category_id>\d+)/$', views.artical_manage, name='cms_artical_manage'),
    url(r'^edit_artical/(?P<pk>[\w\-]+)$', views.edit_artical, name='cms_edit_artical'),
    url(r'^delete_artical/$', views.delete_artical, name='cms_delete_artical'),
    url(r'^top_artical/$', views.top_artical, name='cms_top_artical'),
    url(r'^untop_artical/$', views.untop_artical, name='cms_untop_artical'),
    url(r'^test/$',views.test),
    url(r'^settings/$',views.cms_settings,name='cms_settings'),
    url(r'^update_profile/$',views.update_profile,name='cms_update_profile'),
    url(r'^get_token/$',views.get_token,name='cms_get_token'),
    url(r'^update_email/$',views.update_email,name='cms_update_email'),
    url(r'^email_success/$',views.email_success,name='cms_email_success'),
    url(r'^email_fail/$',views.email_fail,name='cms_email_fail'),
    url(r'^check_email/(?P<code>\w+)$',views.check_email,name='cms_check_email'),
    url(r'^add_category/$',views.add_category,name='cms_add_category'),
    url(r'^category_manage/$',views.category_manage,name='cms_category_manage'),
    url(r'^delete_category/$',views.delete_category,name='cms_delete_category'),
    url(r'^edit_category/$',views.edit_category,name='cms_edit_category'),
    url(r'^add_tag/$',views.add_tags,name='cms_add_tag'),
]
