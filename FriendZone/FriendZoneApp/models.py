from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class HobbyManager(models.Manager):
    def get_by_natural_key(self, hobby):
        return self.get(hobby=hobby)

class Hobby(models.Model):
    objects = HobbyManager()

    hobby = models.CharField(max_length= 20, choices = (('Gaming', 'Gaming'), ('Sports', 'Sports'), 
    ('Reading', 'Reading'), ('Hiking', 'Hiking'), ('Cycling', 'Cycling'), ('Photography', 'Photography'), 
    ('Modelling', 'Modelling')), blank = True)

    def __str__(self):
        return self.hobby

    def natural_key(self):
        return (self.hobby)

class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 254)
    last_name = models.CharField(max_length = 254)
    gender = models.CharField(max_length = 1, choices = (('M', 'Male'), ('F', 'Female')), blank = True)
    age = models.PositiveIntegerField(blank = True, null = True)
    image = models.ImageField(default = 'default.jpg', upload_to='media/profile_images', blank = True)
    dob = models.DateField(blank = True, null = True)
    email = models.EmailField(blank = True, unique = True)
    hobby = models.ManyToManyField(Hobby, blank = True)
    friend = models.ManyToManyField('self', blank = True)
    profileBio = models.CharField(max_length=254, blank = True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
