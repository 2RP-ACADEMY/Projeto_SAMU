from django.db import models
from .vehicleModel import Vehicle

class Material(models.Model):

  """
  Model for representing a material item.

  Attributes:
    id (OneToOneField): A reference to the related Item as a primary key.

    name (CharField): The name of the material (max length: 100, not nullable).

    description (CharField): A description of the material (max length: 300).

    batch_code (CharField): The batch code of the material (max length: 30, not nullable).

    allocable (BooleanField): Indicates if the material is allocable (not nullable).
    
    expiration_date (DateField): The expiration date of the material (nullable).
  """

  id = models.OneToOneField('Item', primary_key=True, on_delete=models.CASCADE, related_name="material")
  description = models.CharField(max_length=300)
  batch_code = models.CharField(max_length=30, null=False, unique=True)
  allocable = models.BooleanField(null=False)
  expiration_date = models.DateField(null=True)
  
def __str__(self):
    return self.name