from django.db import models

class RequestStatus(models.Model):

    """
    Model for representing a request status.

    Attributes:
        name (CharField): The name of the request status (max length: 15, unique).
    """

    name = models.CharField(max_length=15, unique=True)