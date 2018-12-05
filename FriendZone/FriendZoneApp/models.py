from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Hobby(models.Model):
    hobby = models.CharField(max_length= 20, choices = (('Gaming', 'Gaming'), ('Sports', 'Sports'), 
    ('Reading', 'Reading'), ('Hiking', 'Hiking'), ('Cycling', 'Cycling'), ('Photography', 'Photography'), 
    ('Modelling', 'Modelling')), blank = True)

class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length = 1, choices = (('M', 'Male'), ('f', 'Female')), blank = True)
    age = models.PositiveIntegerField(blank = True, null = True)
    hobby = models.ManyToManyField(Hobby, blank = True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
