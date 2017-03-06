from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    #This line is required. Links UserProfile to a User Model Instance
    user = models.OneToOneField(User)


    #The additional attribute we wish to include
    full_name = models.CharField(max_length=100, default='', blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(default='Tell Us About Yourself...', blank=True)




    #Override the __unicode__() method to return out something meaningful

    def __str__(self):
        return self.user.username

