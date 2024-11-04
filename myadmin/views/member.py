# 会员信息管理视图文件

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
import time

from myadmin.models import Member # 用Models连接数据库
from utils.common_utils import uploadPicFile

main_page_element = "会员"
member_attributes = ["ID", "昵称", "头像", "联系电话", "当前状态", "添加时间", "修改时间", "操作"]
items_per_page = 10

# Create your views here.
def index(request, pIndex=1):
    '''浏览信息'''
    umod = Member.objects # User.objects gives you access to all the methods for querying the User model.
    # ulist = umod.all() # .all() returns a QuerySet containing all instances of the User model.
    
    '''This is the condition used to filter the QuerySet. 
    It means “select all objects where the status field is less than 9”. 
    The double underscore (__) is used to specify the lookup type, 
    in this case, lt stands for “less than”.'''
    ulist = umod.filter(status__lt=9) 
    # print(ulist)

    saved_search_words = []
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)

    if kw:
        ulist = ulist.filter(name__contains=kw)
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
        'main_page_element':main_page_element,
        'member_attributes':member_attributes,
        'memberlist':list2,
        'pIndex':pIndex,
        'plist':plist,
        'maxPages':maxPages,
        'saved_search_words':saved_search_words
        }
    # print(ulist)

    return render (request, 'myadmin/member/index.html', data)


def add(request):
    '''加载信息添加表单'''
    data = {
    'main_page_element':main_page_element,
    }
    return render(request, "myadmin/member/add.html", data)


def insert(request):
    '''执行信息添加'''
    try:
        # 实例化model，封装信息，并执行添加操作
        ob = Member() 
        ob.nickname = request.POST['nickname']
        ob.avatar = uploadPicFile(request, "avatar", "member", "没有会员上传文件信息")
        ob.mobile = request.POST['mobile']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save() 
        context = {'info':"添加成功！"}
    except Exception as err:
        print(err)
        context = {'info':"添加失败.."}

    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    '''执行信息删除'''
    try:
        ob = Member.objects.get(id=uid)
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
        ob = Member.objects.get(id=uid)
        data = {'member':ob, 'main_page_element':main_page_element}
        return render(request, "myadmin/member/edit.html", data)

    except Exception as err:
        print(err)
        data = {'info':"没有找到需要修改的信息。"}
        return render(request, "myadmin/info.html", data)

def update(request, uid=0): 
    '''执行信息编辑（修改）'''
    try:
        ob = Member.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.mobile = request.POST['mobile']
        ob.status = request.POST['status']

        oldPicFile = ob.avatar
        avatar = uploadPicFile(request, "avatar", "member", "没有头像上传文件信息", oldPicFile, defaultPicName="moren")
        print("avatar: ", avatar)

        if avatar != "NO_PIC_UPLOADED":
            ob.avatar = avatar

        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ob.save() 
        context = {'info':"修改成功！"}
    except Exception as err:
        print(err)
        context = {'info':"修改失败.."}

    return render(request, "myadmin/info.html", context)
    