# 订单信息管理视图文件

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator

# 导入表格
from myadmin.models import Orders, OrderDetail, Payment, User

items_per_page = 10


def index(request, pIndex=1):
    ''' 浏览订单详情 '''
    umod = Orders.objects
    sid = request.session['shopinfo']['id']
    ulist = umod.filter(shop_id=sid) 

    # Assuming 'Orders' is your model
    shop_id_field = Orders._meta.get_field('shop_id')
    print(shop_id_field.get_internal_type())  # Outputs the internal type of the field

    saved_search_words = []
    # 获取并判断搜索条件
    status = request.GET.get('status', '')

    if status != '':
        ulist = ulist.filter(status=status)
        saved_search_words.append("status=" + status)

    ulist = ulist.order_by("id")

    maxItems = len(ulist)

    # 执行分页处理    
    pIndex = int(pIndex)
    pages = Paginator(ulist, items_per_page)
    maxPages = pages.num_pages # 获取最大页数
    # 判断当前是否越界
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1

    list2 = pages.page(pIndex)  #获取当前页数据
    # plist provides the range of page numbers for navigation.
    plist = pages.page_range # 获取页码列表信息, is range(1, 4) here

    for vo in list2:
        userid = vo.user_id
        if userid == 0:
            vo.nickname == "N/A"
        else:
            user = User.objects.only("nickname").get(id=userid)
            vo.nickname = user.nickname
        
    data = {
        'orderslist':list2,
        'pIndex':pIndex,
        'plist':plist,
        'maxPages':maxPages,
        'maxItems':maxItems,
        'saved_search_words':saved_search_words,
        'orderStatus':status,
        }

    print("Type of list2:::::::::", type(list2))
    print("length of list2:::::::::", len(list2.object_list))
    print("item list of list2:::::::::", list2.object_list)
    # print("orders list:::::::::", list2.object_list[0].__dict__)
    # print("orders list:::::::::", list2.object_list[0].__dict__.keys())
    print("session's keys ::::::", dict(request.session).keys())

    return render (request, 'web/list.html', data)


def insert(request):
    ''' 执行订单添加 '''
    try:
        # 订单模型
        ob = Orders() 
        ob.shop_id = request.session['shopinfo']['id']
        ob.member_id = 0
        ob.user_id = request.session['webuser']['id']
        ob.money = request.session['total_cart_value']

        ob.status = 1   # 订单状态:1进行中/2.无效/3.已完成
        ob.payment_status = 2    # 支付状态:1.未支付/2.已支付/3.已退款
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()

        # 支付信息模型
        op = Payment()
        op.order_id = ob.id
        op.member_id = 0
        op.money = request.session['total_cart_value']
        
        op.type = request.GET.get("ptype", 2)  # 支付方式：1.会员付款/2.收银收款
        op.bank = request.GET.get("bank", 3)    #收款银行渠道：1.微信/2.余额/3.现金/4.支付宝

        op.status = 1   # 订单状态:1进行中/2.无效/3.已完成
        op.payment = 2    # 支付状态:1.未支付/2.已支付/3.已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        # 订单详情模型
        cartlist = request.session.get("cartlist", {})
        for item in cartlist.values():
            dd = OrderDetail()
            dd.order_id = ob.id
            dd.product_id = item['id']
            dd.product_name = item['name']
            dd.price = item['price']
            dd.quantity = item['quantity']
            dd.status = 1   # 订单状态:1.正常/9.删除
            dd.save()
        
        del request.session['cartlist']
        del request.session['total_cart_value']

        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")


def detail(request):
    ''' 加载订单详情 '''
    oid = request.GET.get('oid', 0)
    dlist = OrderDetail.objects.filter(order_id=oid)
    context = {
        "detaillist":dlist,
    }
    return render(request, "web/detail.html", context)


def status(request):
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get('oid', 0)
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")


