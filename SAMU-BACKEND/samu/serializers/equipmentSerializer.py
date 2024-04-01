from rest_framework import serializers
from samu.models.equipmentModel import Equipment
from samu.models.itemModel import Item
from samu.serializers.entrySerializer import EntrySerializer

class EquipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Equipment model.

    Used to serialize and deserialize Equipment objects.
    """
    class Meta:
        model = Equipment
        fields = '__all__'

class EquipmentFullSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Equipment with related entries.

    Used to serialize Equipment objects with associated entries.
    """
    equipment = EquipmentSerializer(read_only=True)
    entries = EntrySerializer(read_only=True, many=True)
    
    class Meta:
        model = Item
        fields = ['equipment', 'entries']
