from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def index(request):
    ''' 个人中心首页 '''
    return render(request, 'mobile/member.html')


def orders(request):
    ''' 个人中心浏览订单 '''
    return render(request, 'mobile/member-orders.html')


def detail(request):
    ''' 个人中心的订单详情 '''
    return render(request, 'mobile/member-order-detail.html')


def logout(request):
    ''' 执行会员退出 '''
    del request.session['mobileuser']
    return render(request, 'mobile/register.html')


def profile(request):
    ''' 会员信息 '''
    return render(request, 'mobile/member-profile.html')
