
from django.conf.urls import url
from .views import home,account

urlpatterns = [
    url(r'^login.html$', account.login),
    # url(r'^xiaoyun.html$', account.xiaoyun),
    # url(r'^shizhengwen.html$', account.shizhengwen),
    url(r'^cunzhang.html$', account.cunzhang),
    url(r'^laocunzhang.html$', account.laocunzhang),
    url(r'^loadeditor$', account.loadeditor),
    url(r'^logout.html$', account.logout),
    url(r'^register.html$', account.register),
    url(r'^check_code.html$', account.check_code),
    url(r'^all/(?P<article_type_id>\d+).html$', home.index, name='index'),
    url(r'^(?P<site>\w+).html$', home.home),
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*).html$', home.filter),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$', home.detail),
    url(r'^', home.index),

]