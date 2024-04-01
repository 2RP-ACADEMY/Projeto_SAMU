from rest_framework import serializers
from samu.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'password', 'is_deleted']
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {'write_only': True}, 'is_superuser': {'write_only': True}, 'is_deleted': {'write_only': True}}

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

        