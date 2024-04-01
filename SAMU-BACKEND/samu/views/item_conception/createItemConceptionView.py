from rest_framework import viewsets
from rest_framework.response import Response
from samu.serializers.itemConceptionSerializer import ItemConceptionSerializer
from utils.string_helpers import sanitize_data


class CreateItemConceptionView(viewsets.ViewSet):

    def create(self, request):
        data = sanitize_data(request.data)
        vehicle = ItemConceptionSerializer(
            data = {
                "name": data.get('name'),
            }
        )

        vehicle.is_valid(raise_exception=True)

        vehicle.save()
        
        return Response({"detail": "Veículo criado com sucesso!", "object": vehicle.data, "code": 201}, status=201)
