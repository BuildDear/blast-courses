from django.contrib.auth.models import UserManager as BaseUserManager, AbstractUser
from django.db import models


class Course(models.Model):

    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=200)


    class Meta:
        db_table = "course"
