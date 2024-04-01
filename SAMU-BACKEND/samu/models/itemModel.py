from django.db import models


class itemType(models.IntegerChoices):

    """
    Enumeration class for defining item types.

    Attributes:
        MEDICINE (int): Represents a medicine item type with a value of 1.

        MATERIAL (int): Represents a material item type with a value of 2.

        EQUIPMENT (int): Represents an equipment item type with a value of 3.
    """

    MEDICINE = 1, "medicine"
    MATERIAL = 2, "material"
    EQUIPMENT = 3, "equipment"


class Item(models.Model):

    """
    Model for representing an item in a database.

    Attributes:
        type (IntegerField): The type of the item, chosen from ItemType choices (nullable).
    """
    item_conception = models.ForeignKey('ItemConception', on_delete=models.CASCADE, related_name="item_conception")
    type = models.IntegerField(choices=itemType.choices, null=True)
