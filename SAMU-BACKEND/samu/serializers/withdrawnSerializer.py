from rest_framework import serializers
from ..models.withdrawnModel import Withdrawn

class WithdrawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawn
        fields = '__all__'