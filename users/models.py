from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'user'),
    )

    email = models.EmailField(db_index=True, unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)

    REQUIRED_FIELDS = ('first_name', 'last_name', 'password')

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "user"

