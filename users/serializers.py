from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        """
        Hash password on creation
        """
        return make_password(value)

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')  # Видаляємо user_type з validated_data
        user = User.objects.create_user(**validated_data)
        user.user_type = user_type  # Присвоюємо значення user_type
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type')
