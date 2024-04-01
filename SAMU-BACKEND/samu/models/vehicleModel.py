import re
from django.core.exceptions import ValidationError
from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
import re

class Vehicle(models.Model):
    # Function to validate vehicle license plate.
    def validate_license_plate(value):
        # Validation with regex, wich is certain that plate contains numbers and letters.
        if not re.match(r'^\w+$', value):
            raise ValidationError('Certifique-se de que a placa contenha números e letras.')
        # Certificate that license is 7 characters.
        if len(value) > 7:
            raise ValidationError('Certifique-se de que esta placa não tenha mais de 7 caracteres.')
        
    """
    Model for representing a vehicle.

    Attributes:
        available (BooleanField): Indicates if the vehicle is available (default: True).
    """
    
    name = models.CharField(max_length=60)
    license_plate = models.CharField(max_length=7, unique=True, validators=[validate_license_plate])
    available = models.BooleanField(default=True)

    


    
