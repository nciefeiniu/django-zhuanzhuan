"""
@UpdateTime: 2017/12/7
@Author: liutao
"""

from django.db import models

# Create your models here.

#产品表
class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=150)
    p_money = models.IntegerField()
    p_number = models.IntegerField()
    p_info = models.TextField()
    u = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'product'


#用户表
class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=50)
    u_passwd = models.CharField(max_length=50)
    u_touxiang = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'user'

#图片表
class Images(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_address = models.CharField(max_length=200)
    p_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'images'


#订单表
class Order(models.Model):
    o_id = models.AutoField(primary_key=True)
    p_id = models.IntegerField()
    u_id = models.IntegerField()
    b_id = models.IntegerField()
    p_name = models.CharField(max_length=100)
    p_money = models.IntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'order'

