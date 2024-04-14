from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    icon_url = models.CharField(max_length=128, null=True)# Sử dụng DateTimeField để tạo ra một trường kiểu String dạng Datetime
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_thumbnail = models.CharField(max_length=500)
    # Sử dụng FloatField, IntegerField để tạo trường kiểu số
    product_price = models.FloatField()
    discount = models.IntegerField()
    amount = models.IntegerField()
    is_public = models.BooleanField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products', null=False)
    product_rate = models.IntegerField()
    product_made = models.CharField(max_length=50)
    product_brand = models.CharField(max_length=50)
    product_genuine = models.BooleanField()
    product_best = models.BooleanField()
    product_des = models.CharField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank = True)


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    inven_product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="inventories",null=False)
    inven_amount = models.IntegerField()

class Meta:
    # Sắp xếp mặc định khi query là giảm dần theo ngày tạo
    ordering = ['-created_at']
    indexes = [
    # Chỉ mục index sẽ đánh theo field created_at
    models.Index(fields=['created_at'])
    ]

class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=128)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
    related_name='product_images', null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)

class ProductComment(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    comment = models.CharField(max_length=512)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
    related_name='product_comments', null=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,null=False)
    quantity_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

