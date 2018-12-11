from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from FriendZoneApp.models import UserProfileModel

class EditProfileForm(UserChangeForm):
    class Meta:
        model = UserProfileModel
        fields = [
            'email',
            'first_name',
            'last_name',
            'gender',
            'image',
            'hobby'
        ]

