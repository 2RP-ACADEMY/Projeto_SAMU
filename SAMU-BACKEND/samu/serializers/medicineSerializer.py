from rest_framework import serializers
from samu.models import Medicine
from samu.models.itemModel import Item
from samu.serializers.entrySerializer import EntrySerializer


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"


class MedicineFullSerializer(serializers.ModelSerializer):
    medicine = MedicineSerializer(read_only=True)
    entries = EntrySerializer(read_only=True, many=True)

    class Meta:
        model = Item
        fields = ["medicine", "entries"]
