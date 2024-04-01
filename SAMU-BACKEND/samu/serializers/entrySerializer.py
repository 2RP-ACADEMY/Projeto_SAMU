from rest_framework import serializers
from samu.models.entryModel import Entry


class EntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the Entry class.

    Used to serialize and deserialize Entry objects.
    """

    class Meta:
        model = Entry
        fields = "__all__"
        extra_kwargs = {"item": {"write_only": True}}


class EntryFullSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for the Entry class.

    Used to serialize Entry objects with additional information.
    """

    expiration_date = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = [
            "id",
            "name",
            "date",
            "quantity",
            "available_quantity",
            "vehicle_id",
            "expiration_date",
        ]

    def get_expiration_date(self, obj):
        """
        Get the expiration date based on the item type.

        Args:
            obj (Entry): The Entry object.

        Returns:
            date: The expiration date or None.
        """
        item_type = obj.item.type
        if item_type == 1:
            return obj.item.medicine.expiration_date
        elif item_type == 2:
            return obj.item.material.expiration_date
        elif item_type == 3:
            return None

    def get_name(self, obj):
        return obj.item.item_conception.name
