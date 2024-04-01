from rest_framework import serializers
from samu.models.materialModel import Material
from samu.models.itemModel import Item
from samu.serializers.entrySerializer import EntrySerializer

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'   

class MaterialFullSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)
    entries = EntrySerializer(read_only=True, many=True)
    
    class Meta:
        model = Item
        fields = ['material', 'entries']