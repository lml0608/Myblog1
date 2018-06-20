from django.conf.urls import url

from .views import user
from .views import trouble
urlpatterns  = [


    url(r'^index.html$', user.index),
    # url(r'^base-info.html$', views.base_info),
    # url(r'^tag.html$', views.tag),
    url(r'^category.html$', user.category),
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', user.article,name='article'),


    #一般用户：提交报账单

    url(r'^trouble-list.html$', trouble.trouble_list),
    #创建
    url(r'^trouble-create.html$', trouble.trouble_create),
    #编辑
    url(r'^trouble-edit-(\d+).html$', trouble.trouble_edit),
    url(r'^trouble-kill-list.html$', trouble.trouble_kill_list),
    url(r'^trouble-kill-(\d+).html$', trouble.trouble_kill),
]