from django.db import models
from .vehicleModel import Vehicle
from django.utils import timezone

class Ocurrence(models.Model):
    """
    Model for representing an ocurrence in a database.

    Attributes:
        vehicle (IntegerField): The vehicle of ocurrence.
        start_datetime (datetime): date and time of ocurrence was started
        end_datetime (datetime): date and time of ocurrence was closed
    """
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start_datetime = models.DateTimeField(default=timezone.now())
    end_datetime = models.DateTimeField(null=True)