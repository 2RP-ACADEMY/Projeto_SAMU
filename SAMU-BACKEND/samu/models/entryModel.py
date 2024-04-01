from django.db import models
from .itemModel import Item
from .vehicleModel import Vehicle
from django.utils.timezone import now


class Entry(models.Model):
    """
    Database model to represent entries.

    This model defines fields to record information about each entry.

    Attributes:
        item (ForeignKey): A foreign key to the 'Item' model, relating the entry to a specific item.
                           When an Item is deleted, related entries are also deleted (on_delete=models.CASCADE).
        date (DateField): A date representing when the entry occurred.
        quantity (IntegerField): The quantity of items in the entry.
        available_quantity (IntegerField): The quantity of items available after the entry.
        vehicle_id (ForeignKey): A foreign key to the 'Vehicle' model, relating the entry to a specific vehicle.
                                 When a Vehicle is deleted, the 'vehicle_id' in this entry is set to NULL (on_delete=models.SET_NULL, null=True).
    """

    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="entries")
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
