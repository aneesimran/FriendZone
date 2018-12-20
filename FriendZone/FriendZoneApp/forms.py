from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from FriendZoneApp.models import UserProfileModel
from django.contrib.auth import authenticate
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

class EditProfileForm(UserChangeForm):
    class Meta:
        model = UserProfileModel
        fields = [
            'email',
            'first_name',
            'last_name',
            'gender',
            'image',
            'hobby',
            'profileBio'
        ]


class DateInput(forms.DateInput):
    input_type = 'date'

class RegisterForm(forms.ModelForm):

    class Meta:
        model = UserProfileModel
        # Add all the fields you want a user to change
        fields = [
            'email',
            'first_name',
            'last_name',
            'gender',
            'image',
            'hobby',
            'dob'
        ]
        widgets = {'dob' : DateInput()}

    
