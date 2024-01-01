from django.contrib import admin
from userauthentication.models import User, ContactUs, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','bio']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'subject', 'message']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'bio', 'phone']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactAdmin)
admin.site.register(Profile, ProfileAdmin)