from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'author']
        read_only_fields = ['author']  # Робимо поле author доступним лише для читання
