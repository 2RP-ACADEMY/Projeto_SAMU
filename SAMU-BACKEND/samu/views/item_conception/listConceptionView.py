from rest_framework import viewsets
from rest_framework.response import Response
from samu.serializers.vehicleSerializer import VehicleSerializer
from samu.models.itemConceptionModel import ItemConception

class ListItemConceptionView(viewsets.ViewSet):
    def list(self, request):
        filtered_queryset = ItemConception.objects.all()
        serializer_entries = VehicleSerializer(filtered_queryset, many=True)

        return Response({"detail": "Veículos retornados com sucesso!", "object": serializer_entries.data, "code": 200}, status=200)
        