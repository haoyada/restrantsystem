"""
子路由
project urls.py -> app urls.py (myadmin/urls.py in this case)

"""
from django.contrib import admin
from django.urls import path

from myadmin.views import index
from myadmin.views import user
from myadmin.views import shop
from myadmin.views import category
from myadmin.views import product
from myadmin.views import member

urlpatterns = [
    path('', index.index, name="myadmin_index"), # 后台首页

    # 后台管理员登录、退出路由
    path('login', index.login, name="myadmin_login"), # 登录页面
    path('exe_login', index.exe_login, name="myadmin_exe_login"), # 执行登录
    path('logout', index.logout, name="myadmin_logout"), # 退出页面
    path('verify', index.verify, name="myadmin_verify"), # 验证码

    # 员工信息管理路由
    path('user/', user.index, {'pIndex': 1}, name="myadmin_user_index_default"), 
    path('user/<int:pIndex>', user.index, name="myadmin_user_index"), # 浏览
    path('user/add', user.add, name="myadmin_user_add"), # 添加表单
    path('user/insert', user.insert, name="myadmin_user_insert"), # 执行添加
    path('user/delete/<int:uid>', user.delete, name="myadmin_user_delete"), # 执行删除
    path('user/edit/<int:uid>', user.edit, name="myadmin_user_edit"), # 加载编辑表单
    path('user/update/<int:uid>', user.update, name="myadmin_user_update"), # 执行编辑

    # 店铺信息管理路由
    path('shop/', shop.index, {'pIndex': 1}, name="myadmin_shop_index_default"), 
    path('shop/<int:pIndex>', shop.index, name="myadmin_shop_index"), # 浏览
    path('shop/add', shop.add, name="myadmin_shop_add"), # 添加表单
    path('shop/insert', shop.insert, name="myadmin_shop_insert"), # 执行添加
    path('shop/delete/<int:uid>', shop.delete, name="myadmin_shop_delete"), # 执行删除
    path('shop/edit/<int:uid>', shop.edit, name="myadmin_shop_edit"), # 加载编辑表单
    path('shop/update/<int:uid>', shop.update, name="myadmin_shop_update"), # 执行编辑


    # 菜品类别信息管理路由
    path('category/', category.index, {'pIndex': 1}, name="myadmin_category_index_default"), 
    path('category/<int:pIndex>', category.index, name="myadmin_category_index"), # 浏览
    path('category/add', category.add, name="myadmin_category_add"), # 添加表单
    path('category/insert', category.insert, name="myadmin_category_insert"), # 执行添加
    path('category/delete/<int:uid>', category.delete, name="myadmin_category_delete"), # 执行删除
    path('category/edit/<int:uid>', category.edit, name="myadmin_category_edit"), # 加载编辑表单
    path('category/update/<int:uid>', category.update, name="myadmin_category_update"), # 执行编辑

    # 菜品信息管理路由
    path('product/', product.index, {'pIndex': 1}, name="myadmin_product_index_default"), 
    path('product/<int:pIndex>', product.index, name="myadmin_product_index"), # 浏览
    path('product/add', product.add, name="myadmin_product_add"), # 添加表单
    path('product/insert', product.insert, name="myadmin_product_insert"), # 执行添加
    path('product/delete/<int:uid>', product.delete, name="myadmin_product_delete"), # 执行删除
    path('product/edit/<int:uid>', product.edit, name="myadmin_product_edit"), # 加载编辑表单
    path('product/update/<int:uid>', product.update, name="myadmin_product_update"), # 执行编辑

    path('product/get-categories/', product.get_categories, name='get_categories'),


    # 会员信息管理路由
    path('member/', member.index, {'pIndex': 1}, name="myadmin_member_index_default"), 
    path('member/<int:pIndex>', member.index, name="myadmin_member_index"), # 浏览
    path('member/add', member.add, name="myadmin_member_add"), # 添加表单
    path('member/insert', member.insert, name="myadmin_member_insert"), # 执行添加
    path('member/delete/<int:uid>', member.delete, name="myadmin_member_delete"), # 执行删除
    path('member/edit/<int:uid>', member.edit, name="myadmin_member_edit"), # 加载编辑表单
    path('member/update/<int:uid>', member.update, name="myadmin_member_update"), # 执行编辑
]
