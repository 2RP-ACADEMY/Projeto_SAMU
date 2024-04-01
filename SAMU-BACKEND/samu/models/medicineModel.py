from django.db import models
from samu.models.itemModel import Item


class Medicine(models.Model):
    class Presentation(models.IntegerChoices):
        PILLS = 1, "Comprimidos"
        POWDER = 2, "Pós"
        CAPSULES = 3, "Cápsulas"
        SYRUPS = 4, "Xaropes"
        SOLUTIONS = 5, "Soluções"
        INJECTABLES = 6, "Injetáveis"
        SPRAYS = 7, "Sprays"
        GELS = 8, "Géis"
        LOTIONS = 9, "Cremes"
        OINTMENT = 10, "Pomadas"

    class Measurement(models.IntegerChoices):
        G = 1, "Grama"
        MG = 2, "Miligrama"
        L = 3, "Litro"
        ML = 4, "Mililitro"

    id = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True, related_name="medicine")
    description = models.CharField(max_length=300, null=True)
    measurement_unit = models.IntegerField(choices=Measurement.choices, null=False)
    presentation = models.IntegerField(choices=Presentation.choices, null=False)
    batch_code = models.CharField(max_length=30, unique=True, null=False)
    concentration = models.CharField(max_length=60)
    therapeutic_class = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
