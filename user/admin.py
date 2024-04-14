from django.contrib import admin
from .models import UserAccount 


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ()
    search_fields = ('first_name',)

admin.site.register(UserAccount, UserAccountAdmin)