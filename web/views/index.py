from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from myadmin.models import User, Shop, Category, Product

# from django.templatetags.static import static
from utils.common_utils import verifies

import hashlib


css_1 = 'web/css/bootstrap.min.css'
# csss_1 = static('web/css/bootstrap.min.css')

img_1 = 'web/images/timg.jpg'
img_2 = 'web/images/verify.png'


# Create your views here.
def index(request):
    '''项目前台大堂点餐首页'''
    return redirect(reverse("web_index"))


def webindex(request):
    '''项目前台大堂点餐首页'''

    cartlist = request.session.get('cartlist',{})

    total_cart_value = 0

    for item in cartlist.values():
        item_value = item['price'] * item['quantity']
        total_cart_value = total_cart_value + item_value

    print("total::::::", total_cart_value)

    request.session['total_cart_value'] = total_cart_value

    context = {
        'img_1':img_1,
        # 'categorylist':request.session.get('categorylist',{}).items(),
        'categorylist':request.session.get('categorylist',{}).values(),
        # 'total_cart_value':total_cart_value,
    } 

    print("cartlist @ loading index:::", cartlist)
    


    # print(request.session['categorylist'].items())
    
    # cate = request.session.get('categorylist',{}).items()
    # for key, category in cate:
    #     print("key", key)
    #     print("cate: ", category)

    return render(request, "web/index.html", context)


def login(request):
    '''load login page'''
    shoplist = Shop.objects.filter(status=1)

    context = {
        'shoplist':shoplist,
        'img_2':img_2,
    } 
    return render(request, "web/login.html", context)


def exe_login(request):
    '''execute login'''
    try:
        # 没有选择店铺
        if request.POST['shop_id'] == '0':
            return redirect(reverse('web_login') + "?errinfo=1")

        # if request.POST['code'] != request.session['verifycode']:
        #     return redirect(reverse('web_login') + "?errinfo=2")

        # 根据登录账号获取登录者信息：
        user = User.objects.get(username=request.POST['username'])
        # 判断当前用户是否是管理员或正常：
        if user.status == 6 or user.status == 1:
            md5 = hashlib.md5()
            s = request.POST['password'] + user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                print("登录成功！")
                # 登录成功后将用户信息以'webuser'为key写入session中：
                request.session['webuser'] = user.toDict()
                # get restaurant ingo, put in session
                shopob = Shop.objects.get(id=request.POST['shop_id'])
                request.session['shopinfo'] = shopob.toDict()
                # get category info
                clist = Category.objects.filter(shop_id=shopob.id, status=1)
                categorylist = dict()
                productlist = dict()
                for vo in clist:
                    c = {'id':vo.id, 'name':vo.name, 'pids':[]}
                    plist = Product.objects.filter(category_id=vo.id, status=1)
                    for p in plist:
                        c['pids'].append(p.toDict())
                        productlist[p.id] = p.toDict()
                    categorylist[vo.id] = c
                # 将结果写入session
                request.session['categorylist'] = categorylist
                request.session['productlist'] = productlist
                # print(type(request.session['categorylist']))

                # for cat in categorylist.values():
                #     print("cat in cate:", cat)

                return redirect(reverse("web_index"))
            else:
                return redirect(reverse('web_login') + "?errinfo=5")
                # context = {'info':"错误的登录密码"}
        else:
            return redirect(reverse('web_login') + "?errinfo=4")
            # context = {'info':"无效的登录账号"}

    except Exception as err:
        print(err)
        return redirect(reverse('web_login') + "?errinfo=3")
        # context = {'info':"登录账号不存在"}

    # return render(request,'myadmin/index/login.html', context)


def logout(request):
    '''execute login'''
    del request.session['webuser']
    return redirect(reverse('web_login'))

def verify(request):
    '''execute login'''
    return verifies(request)
