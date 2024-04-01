from rest_framework import viewsets, status
from samu.models.equipmentModel import Equipment
from samu.serializers import EquipmentSerializer, EquipmentFullSerializer
from rest_framework.response import Response
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from ..items.createItemView import CreateItemView
from ..entries.createEntryView import CreateEntryView
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import PermissionDenied
from utils.string_helpers import sanitize_data


class CreateEquipamentView(viewsets.ViewSet):
    queryset_create = Equipment.objects.all()
    serializer_class_create = EquipmentSerializer
    full_serializer_class_create = EquipmentFullSerializer

    @swagger_auto_schema(
        operation_description="Create a new Equipment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the equipment"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Description of the equipment"
                ),
                "patrimony": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Patrimony number"
                ),
                "allocable": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="Is allocable"
                ),
                "available": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="Is available"
                ),
                "warranty_expire": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="date",
                    description="Warranty expiration date",
                ),
            },
            required=["name", "patrimony", "allocable"],
        ),
        responses={
            201: openapi.Response("Created successfully", EquipmentSerializer),
            400: "Bad Request",
        },
    )
    def create(self, request):
        try:
            data = sanitize_data(request.data)
            if not data:
                RequestController.set_request_status(
                    request_id=request.request_id, status_id=3
                )
                return Response(
                    {
                        "detail": "Nenhum campo foi enviado no corpo da requisição.",
                        "code": 400,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                item = CreateItemView.create(
                    item_type=3, item_conception=request.data.get("item_conception")
                )
                model_serializer = self.serializer_class_create(
                    data={
                        "id": item.id,
                        "name": data.get("name"),
                        "description": data.get("description"),
                        "patrimony": data.get("patrimony"),
                        "allocable": data.get("allocable"),
                        "available": True,
                        "warranty_expire": data.get("warranty_expire"),
                    }
                )
                model_serializer.is_valid(raise_exception=True)
                model_serializer.save()
                entry = CreateEntryView.create(
                    item_id=item.id,
                    quantity=1,
                )
                model_data = self.full_serializer_class_create(item).data

            RequestController.set_request_status(
                request_id=request.request_id, status_id=2
            )
            return Response(
                {
                    "detail": "Equipamento criado com sucesso!",
                    "object": model_data,
                    "code": 201,
                },
                status=status.HTTP_201_CREATED,
            )

        except (KeyError, ValidationError) as error:
            RequestController.set_request_status(
                request_id=request.request_id, status_id=3
            )
            return Response(
                {
                    "detail": {
                        "error_name": error.__class__.__name__,
                        "error_cause": error.args,
                    },
                    "code": 400,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except PermissionDenied as error:
            RequestController.set_request_status(
                request_id=request.request_id, status_id=3
            )
            return Response(
                {
                    "detail": {
                        "error_name": error.__class__.__name__,
                        "error_cause": error.args,
                    },
                    "code": 403,
                },
                status=403,
            )

        except Exception as error:
            RequestController.set_request_status(
                request_id=request.request_id, status_id=3
            )
            return Response(
                {
                    "detail": {
                        "error_name": error.__class__.__name__,
                        "error_cause": error.args,
                    },
                    "code": 500,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
