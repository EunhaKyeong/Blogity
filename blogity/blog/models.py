from django.db import models

#Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'