from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=100)
    password_salt = models.CharField(max_length=50) # 密码干扰值
    status = models.IntegerField(default=1) # 状态：1.正常；2.禁用；6.管理员; 9.删除。
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id':self.id, 'username':self.username, 'nickname':self.nickname, 'password_hash':self.password_hash, 'password_salt':self.password_salt, 'status':self.status, 'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'), 'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'user'


class Shop(models.Model):
    name = models.CharField(max_length=225)
    cover_pic = models.CharField(max_length=225)
    banner_pic = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    status = models.IntegerField(default=1)
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        shopname = self.name.split("-")
        return {'id':self.id,'name':shopname[0],'shop':shopname[1],'cover_pic':self.cover_pic,'banner_pic':self.banner_pic,'address':self.address,'phone':self.phone,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = 'shop' # 更改表名为shop


# 菜品分类信息模型
class Category(models.Model):
    shop_id = models.IntegerField()
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'category'


# 菜品信息
class Product(models.Model):
    shop_id = models.IntegerField()
    category_id = models.IntegerField()
    cover_pic = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    status = models.IntegerField(default=1)
    create_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id':self.id,'shop_id':self.shop_id,'category_id':self.category_id,'cover_pic':self.cover_pic,'name':self.name,'price':self.price,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "product"  # 更改表名


#会员信息模型
class Member(models.Model):
    nickname = models.CharField(max_length=50)    #昵称
    avatar = models.CharField(max_length=255)    #头像
    mobile = models.CharField(max_length=50)    #电话
    status = models.IntegerField(default=1)        #状态:1正常/2禁用/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'nickname':self.nickname,'avatar':self.avatar,'mobile':self.mobile,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "member"  # 更改表名


# 订单模型
class Orders(models.Model):
    shop_id = models.IntegerField()    # 店铺id
    member_id = models.IntegerField()    # 会员id
    user_id = models.IntegerField()    # 操作员id
    money = models.FloatField()    # 金额
    status = models.IntegerField(default=1)        # 订单状态:1进行中/2.无效/3.已完成
    payment_status = models.IntegerField(default=1)        # 支付状态:1.未支付/2.已支付/3.已退款
    create_at = models.DateTimeField(default=datetime.now)    # 创建时间
    update_at = models.DateTimeField(default=datetime.now)    # 修改时间

    class Meta:
        db_table = "orders"  # 更改表名


# 订单详情模型
class OrderDetail(models.Model):
    order_id = models.IntegerField()    # 订单id
    product_id = models.IntegerField()    # 菜品id
    product_name = models.CharField(max_length=50)    # 菜品名称
    price = models.FloatField()    # 单价
    quantity = models.IntegerField()    # 数量
    status = models.IntegerField(default=1)        # 订单状态:1.正常/9.删除

    class Meta:
        db_table = "order_detail"  # 更改表名


# 支付信息模型
class Payment(models.Model):
    order_id = models.IntegerField()    # 订单id
    member_id = models.IntegerField()    # 会员id
    money = models.FloatField()    # 支付金额
    type = models.IntegerField(default=2)    # 支付方式：1.会员付款/2.收银收款
    bank = models.IntegerField(default=1)   #收款银行渠道：1.微信/2.余额/3.现金/4.支付宝
    status = models.IntegerField(default=1)        # 订单状态:1未支付/2.已支付/3.已退款
    create_at = models.DateTimeField(default=datetime.now)    # 创建时间
    update_at = models.DateTimeField(default=datetime.now)    # 修改时间

    class Meta:
        db_table = "payment"  # 更改表名