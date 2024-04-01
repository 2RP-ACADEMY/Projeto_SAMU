from django.db import models
from django.utils import timezone
from .requestStatusModel import RequestStatus
from .requestTypeModel import RequestType
from .userModel import User

class Request(models.Model):

    """
    Model for representing a request.

    Attributes:
        created_at (DateTimeField): Creates date/time when the request was created (default: current time).
        
        status_id (ForeignKey): A reference to the related RequestStatus, protecting against deletion.

        type_id (ForeignKey): A reference to the related RequestType, protecting against deletion (nullable).

        user_id (ForeignKey): A reference to the related User, set to NULL on user deletion (nullable).
    """

    created_at = models.DateTimeField(default=timezone.now)
    status_id = models.ForeignKey(RequestStatus, on_delete=models.PROTECT)
    type_id = models.ForeignKey(RequestType, on_delete=models.PROTECT, db_column="type_id_id", null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)