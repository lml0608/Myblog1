from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from repository import models
from utils.pagination import Pagination


# Create your views here.


def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """

    article_type_list = models.Article.type_choices

    #print(article_type_list)
    # print(kwargs)

    if kwargs:

        #print(kwargs) #{'article_type_id': '4'}

        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index',kwargs=kwargs)
        #print(base_url)

        #print('aID',article_type_id)
    else:
        article_type_id = None
        base_url = '/'

    data_count = article_list = models.Article.objects.filter(**kwargs).count()


    page_obj = Pagination(request.GET.get('p'),data_count)
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)

    # print(request.session['user_info'])

    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            'page_str': page_str,
        }
    )


def home(request, site):

    print(site)
    blog = models.Blog.objects.filter(site=site).select_related('user').first()

    if not blog:
        return redirect('/')

    #获取博客所有标签
    tag_list = models.Tag.objects.filter(blog=blog)

    #获取博客所有分类

    category_list = models.Category.objects.filter(blog=blog)

    # date_list = models.Article.objects.raw(
    #     'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')
    #
    # print(date_list)


    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    article_list = models.Article.objects.filter(blog=blog).order_by('-nid').all()

    return render(
        request,
        'home.html',
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )

    #return render(request,'home.html')



def filter(request, site, condition, val):


    blog = models.Blog.objects.filter(site=site).select_related('user').first()


    if not blog:
        return redirect('/')


    tag_list = models.Tag.objects.filter(blog=blog)

    category_list = models.Category.objects.filter(blog=blog)

    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    template_name = "home_summary_list.html"
    if condition == "tag":
        template_name = "home_title_list.html"

        article_list = models.Article.objects.filter(tags=val, blog=blog).all()

    elif condition == "category":
        article_list = models.Article.objects.filter(category_id=val, blog=blog).all()

    elif condition == "date":
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y-%%m",create_time)=%s'], params=[val, ]).all()
    else:
        atricle_list = []

    return render(
        request,
        template_name,
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list
        }
    )


def detail(request,site, nid):

    blog = models.Blog.objects.filter(site=site).select_related('user').first()

    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,strftime("%Y-%m",create_time) as ctime from repository_article group by strftime("%Y-%m",create_time)')

    article = models.Article.objects.filter(blog=blog, nid=nid).select_related('category','articledetail').first()

    comment_list = models.Comment.objects.filter(article=article).select_related('reply')



    return render(
        request,
        'home_detail.html',
        {
            'blog': blog,
            'article': article,
            'comment_list': comment_list,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
        }

    )
