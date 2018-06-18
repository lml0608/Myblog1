from django.conf.urls import url

from . import views
urlpatterns  = [


    url(r'^index.html$', views.index),
    # url(r'^base-info.html$', views.base_info),
    # url(r'^tag.html$', views.tag),
    url(r'^category.html$', views.category),
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', views.article,name='article'),


]