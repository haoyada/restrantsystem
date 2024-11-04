
from django.contrib import admin
from django.urls import path, include
from web.views import index, cart, orders

urlpatterns = [
    path('', index.index, name="index"),

    path('login', index.login, name="web_login"), # 登录页面
    path('exe_login', index.exe_login, name="web_exe_login"), # 执行登录
    path('logout', index.logout, name="web_logout"), # 退出页面
    path('verify', index.verify, name="web_verify"), # 验证码

    # 为url路径添加web请求前缀，凡是有此前缀的URL地址必须登录后才可访问。
    path('web/', include([
            path('', index.webindex, name="web_index"), 
            path('cart/add/<str:pid>', cart.add, name="web_cart_add"), 
            path('cart/delete/<str:pid>', cart.delete, name="web_cart_delete"), 
            path('cart/change', cart.change, name="web_cart_change"), 
            path('cart/clear', cart.clearCart, name="web_cart_clear"), 

            # 订单处理路由
            path('orders/<int:pIndex>', orders.index, name="web_orders_index"), 
            path('orders/insert', orders.insert, name="web_orders_insert"), 
            path('orders/detail', orders.detail, name="web_orders_detail"), 
            path('orders/status', orders.status, name="web_orders_status"), 

        ]))
]
