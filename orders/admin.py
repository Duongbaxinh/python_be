from django.contrib import admin
from .models import Order,OrderDetail

class OrderAdmin(admin.ModelAdmin):
    list_display:[]
    search_fields:[]
    list_filter:['date']
admin.site.register(Order,OrderAdmin)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display:[]
    search_fields:[]
    list_filter:['date']
admin.site.register(OrderDetail,OrderDetailAdmin)
# Register your models here.
