from django.contrib import admin
from .models import Product,Category,ProductImage,ProductComment,Inventory
from rest_framework.authtoken.models import Token
class ProductAdmin(admin.ModelAdmin):
    list_display:['product_name','unit','price','is_public']
    search_fields:['product_name']
    list_filter:['date']
admin.site.register(Product,ProductAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display:[]
    search_fields:[]
    list_filter:['date']
admin.site.register(Inventory,InventoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display:[]
    search_fields:[]
    list_filter:['date']
admin.site.register(Category,CategoryAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display:[]
    search_fields:[]
    list_filter:['date']
admin.site.register(ProductImage,ProductImageAdmin)

class ProductCommentAdmin(admin.ModelAdmin):
    list_display:[]
    search_fields:[]
    list_filter:['date']
admin.site.register(ProductComment,ProductCommentAdmin)

# Register your models here.
