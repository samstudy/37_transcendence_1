from django.db import models


class UserInformation(models.Model):
    name = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    birth_day = models.DateField()
    gmail = models.EmailField()
    facebook = models.CharField(max_length=100)
    vk = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
