from io import BytesIO
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from repository import models
from django.urls import reverse
from ..forms.account import LoginForm,RegisterForm
from utils.check_code import create_validate_code
import json

def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登录
    :param request: 
    :return: 
    """
    if request.method == 'GET':
        return render(request,'login.html')


    elif request.method == 'POST':

        result = {'status': False, 'message': None, 'data': None}

        form = LoginForm(request=request,data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user_info = models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('nid','nickname',
                       'username', 'email',
                       'avatar',
                       'blog__nid',
                       'blog__site').first()


            if not user_info:

                result['message'] = '用户名或密码错误'

            else:
                result['status'] = True

                request.session['user_info'] = user_info

                if form.cleaned_data.get('rmb'):

                    request.session.set_expiry(60 * 60 * 24 * 7)

        else:
            print(form.errors)

            if 'check_code' in form.errors:

                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'

        return HttpResponse(json.dumps(result))


def register(request):

    if request.method == 'GET':

        return render(request, 'register.html')

    else:

        form = RegisterForm(request=request,data=request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            return redirect('/login.html')
        else:

            #v.errors
            print(form.errors)

            return render(request,'register.html',{'form':form})

def logout(request):

    request.session.clear()

    return redirect('/')

def cunzhang(request):

    return render(request,'cunzhang.html')

def laocunzhang(request):
    ret = {'status': '','msg': ""}
    print("hellp")
    print(request.POST)
    print(request.FILES)
    dic = {
        'error': 0,
        'url': '/static/imgs/4.jpg',
        'message': '错误了...'
    }

    return JsonResponse(dic)


def loadeditor(request):

    print(request.POST)

    content = request.POST.get("id")

    print(content)

    return JsonResponse({"status":True})