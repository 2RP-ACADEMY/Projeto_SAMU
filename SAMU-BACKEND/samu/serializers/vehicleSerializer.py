from rest_framework import serializers
from samu.models.vehicleModel import Vehicle



class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'





