from email.policy import default
from django.db import models

from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.CharField(null=True, blank=True, max_length=100, default=0)
    content = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    likes = models.CharField(null=True, blank=True, max_length=100)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    content = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.owner.username