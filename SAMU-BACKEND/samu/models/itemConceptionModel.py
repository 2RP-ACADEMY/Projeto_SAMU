from django.db import models

class ItemConception(models.Model):

    """
    Model for representing an itemConception in a database.

    Attributes:
        name (CharField): The name of the item.
    """
    name = models.CharField(max_length=150, unique=True)
