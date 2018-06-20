from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect
from repository import models
from utils.pagination import Pagination
from django.urls import reverse
import datetime


# Create your views here.


def trouble_list(request):


    current_user_id = 1

    result = models.Trouble.objects.filter(user_id=current_user_id).order_by('status').\
        only('title','status','ctime','processer')

    return render(request,'backend_trouble_list.html',{'result':result})

from django.forms import Form
from django.forms import fields
from django.forms import widgets

class TroubleMaker(Form):

    title = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={"class":'form-control'})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'})
    )

def trouble_create(request):

    if request.method == "GET":
        form = TroubleMaker()

    else:

        form = TroubleMaker(request.POST)
        if form.is_valid():

            dic = {}
            dic['user_id'] = 1
            dic['ctime'] = datetime.datetime.now()
            dic['status'] = 1
            dic.update(form.cleaned_data)

            print(dic)

            models.Trouble.objects.create(**dic)

            return redirect('/backend/trouble-list.html')


    return render(request,'backend_trouble_create.html',{'form':form})



def trouble_edit(request,nid):

    if request.method == "GET":

        #查出属于id=nid 并且要是未处理，因为其他人可能正在处理，所有要判断status=1未处理，只需要2个字段
        obj = models.Trouble.objects.filter(id=nid,status=1).only('id','title','detail').first()
        if not obj:

            return HttpResponse("正在处理的保障单无法修改...")
        #initial仅初始化
        form = TroubleMaker(initial={'title':obj.title,'detail':obj.detail})

        return render(request,'backend_trouble_edit.html',{'form':form,'nid':nid})
    else:

        form = TroubleMaker(data=request.POST)

        if form.is_valid():

            v = models.Trouble.objects.filter(id=nid,status=1).update(**form.cleaned_data)

            if not v:
                return HttpResponse("已经被处理")
            else:

                return redirect('/backend/trouble-list.html')


        return render(request,'backend_trouble_edit.html',{'form':form,'nid':nid})



def trouble_kill_list(request):

    from django.db.models import Q

    current_user_id = 1

    result = models.Trouble.objects.filter(Q(processer_id=current_user_id)|Q(status=1)).order_by('status')

    return render(request,'backend_trouble_kill_list.html',{'result':result})









