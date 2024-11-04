# 员工信息管理视图文件

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from myadmin.models import User # 用Models连接数据库
import hashlib, random # for MD5 process of user password

user_attributes = ["ID", "员工账号", "昵称", "当前状态", "添加时间", "修改时间", "操作"]
items_per_page = 5

def process_psw(raw_pw):
    md5 = hashlib.md5()
    n = random.randint(100000, 999999)
    s = raw_pw + str(n)
    md5.update(s.encode('utf-8'))
    return (md5.hexdigest(), n)


# Create your views here.
def index(request, pIndex=1):
    '''浏览信息'''
    umod = User.objects # User.objects gives you access to all the methods for querying the User model.
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
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        saved_search_words.append('keyword=' + kw)

    """ Using None also works. Differences:
        None is used when you want to check for the presence of a parameter.
        '' (empty string) is used when an empty string is a valid value and 
        you want to differentiate it from the absence of the parameter."""

    status = request.GET.get('status', '')

    if status != '':
        ulist = ulist.filter(status=status)
        saved_search_words.append("status=" + status)

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

    data = {
        'user_attributes':user_attributes,
        'userlist':list2,
        'pIndex':pIndex,
        'plist':plist,
        'maxPages':maxPages,
        'saved_search_words':saved_search_words
        }
    # print(ulist)

    return render (request, 'myadmin/user/index.html', data)


def add(request):
    '''加载信息添加表单'''
    return render(request, "myadmin/user/add.html")


def insert(request):
    '''执行信息添加'''
    try:
        # creates a new instance of the User class from your myadmin.models module.
        ob = User() 
        # Assigns the value from the username field in the POST request 
        # to the username attribute of the ob object.
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        ob.status = 1

        # process password using MD5:
        processed_psw = process_psw(request.POST['password'])
        ob.password_hash = processed_psw[0]
        ob.password_salt = processed_psw[1]

        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # saves the current state of the ob object to the database. 
        # It inserts a new record if the object is new or updates 
        # the existing record if the object already exists.
        ob.save() 
        context = {'info':"添加成功！"}
    except Exception as err:
        print(err)
        context = {'info':"添加失败.."}

    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    '''执行信息删除'''
    try:
        ob = User.objects.get(id=uid)
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
        ob = User.objects.get(id=uid)

        data = {'user':ob}
        return render(request, "myadmin/user/edit.html", data)

    except Exception as err:
        print(err)
        data = {'info':"没有找到需要修改的信息。"}
        return render(request, "myadmin/info.html", data)

def update(request, uid=0): 
    '''执行信息编辑（修改）'''
    try:
        ob = User.objects.get(id=uid)

        # ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']

        # ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ob.save() 
        context = {'info':"修改成功！"}
    except Exception as err:
        print(err)
        context = {'info':"修改失败.."}

    return render(request, "myadmin/info.html", context)
    