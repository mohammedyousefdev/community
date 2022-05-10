from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from more_itertools import last


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    bio = models.TextField(max_length=350, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    picture = models.ImageField(default='profile.jpg')
    telegram = models.CharField(max_length=300, null=True, blank=True)
    instagram = models.CharField(max_length=300, null=True, blank=True)
    facebook = models.CharField(max_length=300, null=True, blank=True)
    rating = models.IntegerField(default='0')

    def __str__(self):
        return self.first_name + self.last_name