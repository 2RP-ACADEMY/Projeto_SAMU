from samu.serializers.withdrawnSerializer import WithdrawnSerializer
from samu.models.entryModel import Entry
from samu.serializers.entrySerializer import EntrySerializer
from samu.views.entries.updateEntryView import UpdateEntryView
from django.db import transaction

class WithdrawnController():

    @staticmethod
    def create(entry: Entry, quantity: int, reason: int):
        withdrawn = WithdrawnSerializer(data={
            "entry_id": entry.id,
            "quantity": quantity,
            "reason": reason
        })
        withdrawn.is_valid(raise_exception=True)
        withdrawn.save()
        consumption_data = {
            "quantity": quantity,
            "entry": entry
        }
        UpdateEntryView.consumption(**consumption_data)
        return withdrawn.data
            