# 菜品信息管理视图文件

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from utils.common_utils import uploadPicFile
from myadmin.models import Category, Shop, Product # 用Models连接数据库

from datetime import datetime
import time, os 

main_page_element = "菜品"
product_attributes = ["ID", "店铺名称", "菜品分类", "菜品图片", "菜品名称", "单价", "状态", "添加时间", "修改时间", "操作"]
items_per_page = 10

# Create your views here.
def index(request, pIndex=1):
    '''浏览信息'''
    umod = Product.objects # User.objects gives you access to all the methods for querying the User model.
    # ulist = umod.all() # .all() returns a QuerySet containing all instances of the User model.
    
    '''This is the condition used to filter the QuerySet. 
    It means “select all objects where the status field is less than 9”. 
    The double underscore (__) is used to specify the lookup type, 
    in this case, lt stands for “less than”.'''
    ulist = umod.filter(status__lt=9) 

    saved_search_words = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)

    if kw:
        ulist = ulist.filter(name__contains=kw)
        saved_search_words.append('keyword=' + kw)

    # 根据菜品类别搜索：
    ctgy = request.GET.get('category_id', None)
    if ctgy:
        ulist = ulist.filter(category_id=ctgy)
        saved_search_words.append("category_id=" + ctgy)

    # 根据状态搜索：
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        saved_search_words.append("status=" + status)

    """ Using None also works. Differences:
    None is used when you want to check for the presence of a parameter.
    '' (empty string) is used when an empty string is a valid value and 
    you want to differentiate it from the absence of the parameter."""

    ulist = ulist.order_by("id")

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

    # 夸表搜索，从Shop表中提取店铺名，放到菜品列表中：
    for ele in list2:
        # 取得店铺名称：
        try:
            targetShop = Shop.objects.get(id=ele.shop_id)
            ele.shopname = targetShop.name
        except ObjectDoesNotExist:
            ele.shopname = "该店铺没有在记录中。店铺ID：" + str(ele.shop_id) 
        # 取得菜品种类名称
        try:
            targetCategory = Category.objects.get(id=ele.category_id)
            ele.categoryname = targetCategory.name
        except ObjectDoesNotExist:
            ele.categoryname = "该菜品种类没有在记录中。菜品种类ID：" + str(ele.category_id) 


    data = {
        'main_page_element':main_page_element,
        'product_attributes':product_attributes,
        'productlist':list2,
        'pIndex':pIndex,
        'plist':plist,
        'maxPages':maxPages,
        'saved_search_words':saved_search_words
        }
    # print(ulist)

    return render (request, 'myadmin/product/index.html', data)


def add(request):
    '''加载信息添加表单'''
    # 添加菜品是需要店铺的信息。
    # 提取出店铺Shop中的id和name，以字典形式放入shopList：
    shopList = Shop.objects.values("id", "name")
    categorylist = Category.objects.values("shop_id", "name")
    # print("shoplist:", shopList)
    data = {
        'main_page_element':main_page_element,
        'shoplist':shopList,
        'categorylist':categorylist,
        }
    return render(request, "myadmin/product/add.html", data)


def get_categories(request):
    # AJAX view to get categories based on selected shop
    shop_id = request.GET.get('shop_id')
    # print(shop_id)
    categories = Category.objects.filter(shop_id=shop_id, status=1)
    return JsonResponse({
        'categories': list(categories.values('id', 'name'))
    })


def insert(request):
    '''执行信息添加'''
    try:
        # creates a new instance of the User class from your myadmin.models module.
        ob = Product() 
        # Assigns the value from the username field in the POST request 
        # to the username attribute of the ob object.
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']

        price_str = request.POST.get('price', '0')
        price = float(price_str)
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        ob.price = round(price, 2)

        ob.cover_pic = uploadPicFile(request, "cover_pic", "product", "没有菜品图片上传文件信息")

        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # saves the current state of the ob object to the database. 
        # It inserts a new record if the object is new or updates 
        # the existing record if the object already exists.
        ob.save() 
        context = {'info':"添加成功！"}
    except (ValueError, InvalidOperation) as e:
        messages.error(request, f"Invalid price format. Please enter a valid number: {str(e)}")
        return redirect('add_product')
    except Exception as err:
        print(err)
        context = {'info':"添加失败.."}

    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    '''执行信息删除'''
    try:
        ob = Product.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"删除成功！"}
    except Exception as err:
        print(err)
        context = {'info':"删除失败.."}

    return render(request, "myadmin/info.html", context)

def edit(request, uid=0): 
    '''加载信息编辑表单'''
    try:
        ob = Product.objects.get(id=uid)
        # 提取出Shop中的id和name，以QuerySet形式放入shopList：
        shopList = Shop.objects.values("id", "name")

        categoryList = Category.objects.filter(shop_id=ob.shop_id, status=1)

        # Convert QuerySet to dictionary with id as key
        # shopDict = {shop['id']: shop['name'] for shop in shopList}

        data = {
            'product':ob, 
            'main_page_element':main_page_element,
            'shoplist':shopList,
            'categorylist':categoryList,
            # 'shopdict':shopDict,
            }
        return render(request, "myadmin/product/edit.html", data)

    except Exception as err:
        print(err)
        data = {'info':"没有找到需要修改的信息。"}
        return render(request, "myadmin/info.html", data)

def update(request, uid=0): 
    '''执行信息编辑（修改）'''
    try:
        ob = Product.objects.get(id=uid)

        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.status = request.POST['status']

        price_str = request.POST.get('price', '0')
        price = float(price_str)
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        ob.price = round(price, 2)

        print("old pic:", ob.cover_pic)
        cover_pic = uploadPicFile(request, "cover_pic", "product", "没有菜品图片上传文件信息", ob.cover_pic)
        if cover_pic != "NO_PIC_UPLOADED":
            ob.cover_pic = cover_pic

        # ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ob.save() 
        context = {'info':"修改成功！"}
    except Exception as err:
        print(err)
        context = {'info':"修改失败.."}

    return render(request, "myadmin/info.html", context)
    