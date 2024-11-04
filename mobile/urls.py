
from django.contrib import admin
from django.urls import path
from mobile.views import index, member

urlpatterns = [
    path('', index.index, name="mobile_index"),
    # 会员注册/登录
    path('register', index.register, name="mobile_register"),
    path('exeregister', index.exe_register, name="mobile_exe_register"),
    path('shop', index.shop, name="mobile_shop"),
    path('shop/select', index.selectShop, name="mobile_select_shop"),
    path('orders/add', index.addOrders, name="mobile_add_orders"),

    # 会员中心页
    path('member', member.index, name="mobile_member_index"),
    path('member/orders', member.orders, name="mobile_member_orders"),
    path('member/order-detail', member.detail, name="mobile_member_order_detail"),
    path('member/logout', member.logout, name="mobile_member_logout"),
    path('member/profile', member.profile, name="mobile_member_profile"),
]