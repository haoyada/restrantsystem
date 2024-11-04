from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # print("ShopMiddleware.")

    def __call__(self, request):
        path = request.path
        # print("url: ", path)

        # 后台拦截
        # 判断后台是否登录
        # 判断当前url地址是否是以 /myadmin 开头,并且不在urllist中，才做是否登陆判断：
        # 定义后台不登录 也可以直接访问的url列表：
        urllist = ['/myadmin/login', '/myadmin/logout', '/myadmin/exe_login', '/myadmin/verify']
        if re.match(r'^/myadmin',path) and (path not in urllist):
            # 判断是否登录(key名为adminuser是否存在在session中)：
            if 'adminuser' not in request.session:
                # 重定向到登陆页面：
                return redirect(reverse("myadmin_login"))

        # 前台拦截
        # 判断大堂点餐请求的判断，判断是否登录（session中是否有webuser）
        if re.match(r'^/web', path):
            if 'webuser' not in request.session:
                return redirect(reverse("web_login"))

        # 移动端拦截
        # 判断移动端是否登录
        urllist = ['/mobile/register', '/mobile/exeregister']
        if re.match(r'^/mobile',path) and (path not in urllist):
            # 判断是否登录(key名为mobileuser是否存在在session中)：
            if 'mobileuser' not in request.session:
                # 重定向到登陆页面：
                return redirect(reverse("mobile_register"))
        

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response