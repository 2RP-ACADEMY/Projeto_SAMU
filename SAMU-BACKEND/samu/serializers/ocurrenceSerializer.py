from rest_framework import serializers
from samu.models.ocurrenceModel import Ocurrence

class OcurrenceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ocurrence model.

    Used to serialize and deserialize Ocurrence objects.
    """
    class Meta:
        model = Ocurrence
        fields = '__all__'