from rest_framework import viewsets
from samu.models import Equipment
from samu.serializers import EquipmentSerializer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.db import transaction
from samu.serializers import EquipmentFullSerializer
from samu.models.itemModel import Item
from samu.views.requests.requestController import RequestController
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.string_helpers import sanitize_data


class UpdateEquipmentView(viewsets.ViewSet):
    queryset_update = Equipment.objects.all()
    model_update = Equipment
    serializer_class_update = EquipmentSerializer
    full_serializer_class_update = EquipmentFullSerializer

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
            required=["quantity"],
        ),
        responses={
            201: openapi.Response(
                "Equipment updated successfully", EquipmentSerializer
            ),
            400: "Bad Request",
        },
    )
    def update(self, request, pk=None):
        try:
            data = sanitize_data(request.data)
            if not data:
                raise ValidationError("Nenhum campo foi enviado no corpo da requisição.")
            with transaction.atomic():
                model_update = self.model_update.objects.get(pk=pk)
                updated_model = self.serializer_class_update(
                    model_update, data=data, partial=True
                )
                updated_model.is_valid(raise_exception=True)
                updated_model.save()
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Equipamento atualizado com sucesso!",
                    "object": updated_model.data,
                    "code": 201
                },
                status=201,
            )
        except ValidationError as error:
            # Set the request status to validation error.
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
                    "code": 400
                },
                status=400,
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