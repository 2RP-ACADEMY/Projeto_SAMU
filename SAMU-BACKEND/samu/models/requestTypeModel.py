from django.db import models


class RequestType(models.Model):

    """
    Model for representing a request type.

    Attributes:
        name (CharField): The name of the request type (max length: 50, unique).
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
