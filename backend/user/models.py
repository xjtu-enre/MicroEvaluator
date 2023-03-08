from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    level = models.IntegerField(unique=True, max_length=11, default=0, verbose_name='user level')

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = verbose_name
        ordering = ['id']
