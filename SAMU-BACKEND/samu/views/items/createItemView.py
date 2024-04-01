from samu.models.itemModel import Item
from samu.serializers.itemSerializer import ItemSerializer

class CreateItemView():

    @staticmethod
    def create(item_type: int, item_conception):
        item = ItemSerializer(data={"type": item_type, "item_conception": item_conception})
        item.is_valid(raise_exception=True)
        item.save()
        item = Item.objects.get(pk=item.data['id'])
        return item