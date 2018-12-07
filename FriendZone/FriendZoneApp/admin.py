from django.contrib import admin
from FriendZoneApp.models import UserProfileModel, Hobby

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'age', 'email']

admin.site.register(UserProfileModel, UserProfileAdmin)
admin.site.register(Hobby)