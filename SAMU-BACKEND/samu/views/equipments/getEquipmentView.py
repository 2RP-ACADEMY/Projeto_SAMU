from rest_framework import viewsets, status
from samu.serializers.equipmentSerializer import (
    EquipmentFullSerializer,
)
from samu.models.itemModel import Item
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from samu.views.requests.requestController import RequestController
from django.db import transaction


class GetEquipmentView(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            equipment_data = EquipmentFullSerializer(item)
            
            # Verifica se 'equipment' é null
            if equipment_data.data.get("equipment") is None:
                RequestController.set_request_status(
                    request_id=request.request_id, status_id=3
                )
                return Response(
                    {
                        "detail": "O equipamento requisitado não existe na base de dados.",
                        "code": 404
                    },
                    status=404,
                )
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Equipamento encontrado com sucesso!",
                    "object": equipment_data.data,
                    "code": 200
                },
                status=200,
            )

        except Item.DoesNotExist as error:
            # Set the request status to indicate a user not found error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(
                request_id=request.request_id, status_id=3
            )
            return Response(
                {
                    "detail": {
                        "error_name": error.__class__.__name__,
                        "error_cause": error.args,
                    },
                    "code": 404
                },
                status=404,
            )

        except PermissionDenied as error:
            # Set the request status to indicate a permission error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(
                request_id=request.request_id, status_id=3
            )
            return Response(
                {
                    "detail": {
                        "error_name": error.__class__.__name__,
                        "error_cause": error.args,
                    },
                    "code": 403
                },
                status=403,
            )

        except Exception as error:
            # Set the request status to indicate an internal server error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(
                request_id=request.request_id, status_id=3
            )
            return Response(
                {
                    "detail": {
                        "error_name": error.__class__.__name__,
                        "error_cause": error.args,
                    },
                    "code": 500
                },
                status=500,
            )
