from django.db import models


# Create your models here.
class UserProfile(models.Model):
    userName = models.CharField(max_length = 150)
    password = models.CharField(max_length = 30)
    userProfilePic = models.ImageField()
    email = models.EmailField()

class Profile(models.Model):
    bio = models.CharField(max_length = 2000)
    image = models.ImageField(upload_to = 'profile_image')
