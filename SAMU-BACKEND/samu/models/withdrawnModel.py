from django.db import models
from .entryModel import Entry
from .ocurrenceModel import Ocurrence

class Reasons(models.IntegerChoices):
    CONSUMPTION = 1, "consumo"
    EXPIRATION_DATE = 2, "vencimento"
    LOSS = 3, "perda"
    THEFT = 4, "roubo"
    ALLOCATION = 5, "alocação"
    DEALLOCATION = 6, "desalocação"
    UNKNOWN = 7, "desconhecida"

class Withdrawn(models.Model):
    entry_id = models.ForeignKey(Entry, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    reason = models.IntegerField(choices=Reasons.choices)
    ocurrence = models.ForeignKey(Ocurrence, on_delete=models.PROTECT, null=True)