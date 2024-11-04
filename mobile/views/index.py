from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from myadmin.models import Member

# Create your views here.
def index(request):
    ''' 移动端首页 '''
    return render(request, 'mobile/index.html')


def register(request):
    ''' 会员注册登录页 '''

    return render(request, 'mobile/register.html')


def exe_register(request):
    ''' 移动端执行会员注册登录 '''
    vcode = "1234" # request.session['verifycode']
    
    # if vcode != request.POST['vcode']:
    #     context = {"info":"verify code is wrong.."}
    #     return render(request, 'mobile/register.html', context)
    try:
        member = Member.objects.get(mobile=request.POST['mobile'])
        print("member:::", member)
        if member.status == 1:
            request.session['mobileuser'] = member.toDict()
            return redirect(reverse("mobile_shop"))
        else:
            context = {"info":"Member status invalid."}
            return render(request, 'mobile/register.html', context)
    except Member.DoesNotExist: 
        context = {"info": "Member does not exist."} 
        return render(request, 'mobile/register.html', context)
    except Exception as err:
        print(err)
        context = {"info":"Error in Member"}
        return render(request, 'mobile/register.html', context)




    # return render(request, 'mobile/register.html')



def shop(request):
    ''' 移动端选择店铺页面 '''
    return render(request, 'mobile/shop.html')


def selectShop(request):
    ''' 移动端执行选择店铺 '''
    pass


def addOrders(request):
    ''' 添加订单 '''
    return render(request, 'mobile/addorder.html')