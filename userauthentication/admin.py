from django.contrib import admin
from userauthentication.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','bio']

# Register your models here.
admin.site.register(User, UserAdmin)