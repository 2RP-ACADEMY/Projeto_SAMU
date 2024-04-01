from rest_framework import serializers
from samu.models.itemConceptionModel import ItemConception

class ItemConceptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Item model.

    Used to serialize and deserialize ItemConception objects.
    """
    class Meta:
        model = ItemConception
        fields = ['id', 'name']