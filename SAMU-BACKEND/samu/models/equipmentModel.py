from django.db import models
from .itemModel import Item

class Equipment(models.Model):
    """
    Represents an equipment in the system.
    
    Attributes:
        id (OneToOneField): A relationship with the 'Item' class, used as the primary key.
        
        name (CharField): The name of the equipment with a maximum of 100 characters.
        
        description (CharField): A description of the equipment with a maximum of 300 characters.
        
        patrimony (CharField): The unique patrimony number of the equipment with a maximum of 45 characters.
        
        allocable (BooleanField): Indicates whether the equipment is allocable (True) or not (False).
        
        available (BooleanField): Indicates whether the equipment is available (True) or not (False) by default.
        
        warranty_expire (DateField): The expiration date of the equipment's warranty.
    """

    id = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True, related_name="equipment")
    description = models.CharField(max_length=300)
    patrimony = models.CharField(max_length=45, unique=True, null=True)
    allocable = models.BooleanField(null=False)
    available = models.BooleanField(default=True)
    warranty_expire = models.DateField(null=True)

def __str__(self):
    return self.name