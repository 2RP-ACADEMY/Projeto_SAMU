from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the Group model.

    Used to serialize and deserialize Group objects.
    """
    class Meta:
        model = Group
        fields = '__all__'
        extra_kwargs = {'permissions': {'read_only': True}}