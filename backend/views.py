from django.shortcuts import render

from repository import models
from utils.pagination import Pagination
from django.urls import reverse
from .auth import auth

# Create your views here.

@auth.check_login
def index(request):

    return render(request,'backend_index.html')

def category(request):


    return render(request, 'backend_category.html')

def article(request, *args, **kwargs):


    """
    文章管理
    :param request: 
    :param args: 
    :param kwargs: 
    :return: 
    """


    blog_id = request.session['user_info']["blog__nid"]

    condition = {}

    for k, v in kwargs.items():

        if v == '0':
            pass

        else:

            condition[k] = v

    condition['blog_id'] = blog_id

    print(condition)

    data_count = models.Article.objects.filter(**condition).count()
    page = Pagination(request.GET.get('p', 1), data_count)
    result = models.Article.objects.filter(**condition).order_by('-nid').only('nid', 'title','blog').select_related('blog')[page.start:page.end]
    page_str = page.page_str(reverse('article', kwargs=kwargs))
    category_list = models.Category.objects.filter(blog_id=blog_id).values('nid', 'title')
    type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choices)
    kwargs['p'] = page.current_page
    return render(request,
                  'backend_article.html',
                  {'result': result,
                   'page_str': page_str,
                   'category_list': category_list,
                   'type_list': type_list,
                   'arg_dict': kwargs,
                   'data_count': data_count
                   }
                  )



