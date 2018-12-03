from django.contrib import admin
from FriendZoneApp.models import UserProfileModel

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'age']

admin.site.register(UserProfileModel, UserProfileAdmin)