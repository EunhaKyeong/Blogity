from django.contrib import admin
from blog.models import Account

#Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'password']

admin.site.register(Account, AccountAdmin)