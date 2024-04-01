from rest_framework import serializers
from samu.models.itemModel import Item

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Item model.

    Used to serialize and deserialize Item objects.
    """
    item_type = serializers.SerializerMethodField()

    def get_item_type(self, obj):
        """
        Get the display value of the item type.

        Args:
            obj (Item): The Item object.

        Returns:
            str: The display value of the item type.
        """
        return obj.get_type_display() 

    class Meta:
        model = Item
        fields = ['id', 'type', 'item_type', 'item_conception']
        extra_kwargs = {'item_type': {'read_only': True}, 'type': {'write_only': True}}
