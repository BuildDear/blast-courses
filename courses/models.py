from django.db import models
from django.core.validators import MinLengthValidator

from blast_courses import settings


class Course(models.Model):
    name = models.CharField(unique=True, max_length=20, db_index=True)
    description = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses')

    class Meta:
        db_table = "course"

    def __str__(self):
        return self.name

    def enrolled_users_count(self):
        return self.users.count()
