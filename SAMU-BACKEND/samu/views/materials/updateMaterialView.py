from rest_framework import viewsets
from samu.models.materialModel import Material
from samu.serializers.materialSerializer import MaterialSerializer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.db import transaction
from samu.models.itemModel import Item
from samu.models.materialModel import Material
from samu.views.requests.requestController import RequestController
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.string_helpers import sanitize_data

request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, description="Nome do material"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING, description="Descrição do material"
        ),
        "batch_code": openapi.Schema(
            type=openapi.TYPE_STRING, description="Código do lote"
        ),
        "allocable": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Alocável"),
        "expiration_date": openapi.Schema(
            type=openapi.TYPE_STRING, format="date", description="Data de expiração"
        ),
        "quantity": openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantidade"),
    },
    required=["quantity"],
)


class UpdateMaterialView(viewsets.ViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @swagger_auto_schema(
        request_body=request_body,
        responses={201: "Material atualização com sucesso!"},
        operation_description="Atualiza um  material.",
    )
    def update(self, request, pk=None):
        try:
            data = sanitize_data(request.data)
            if not data:
                raise ValidationError("Nenhum campo foi enviado no corpo da requisição.")
            with transaction.atomic():
                material = Material.objects.get(pk=pk)
                updated_material = MaterialSerializer(material, data=data, partial=True)
                updated_material.is_valid(raise_exception=True)
                updated_material.save()
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Material atualizado com sucesso!",
                    "object": updated_material.data,
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

