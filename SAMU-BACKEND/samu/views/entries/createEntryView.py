from samu.models.entryModel import Entry
from samu.serializers.entrySerializer import EntrySerializer

class CreateEntryView():
    
    @staticmethod
    def create(item_id: int, quantity: int):
        entry = EntrySerializer(
            data={
                "item": item_id,
                "quantity": quantity,
                "available_quantity": quantity
            }
        )
        entry.is_valid(raise_exception=True)
        entry.save()
        return entry.data