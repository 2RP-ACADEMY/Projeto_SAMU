from rest_framework import viewsets
from samu.serializers import MedicineSerializer
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.db import transaction
from samu.models import Item
from samu.models import Medicine
from samu.views.requests.requestController import RequestController
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from utils.string_helpers import sanitize_data

class UpdateMedicineView(viewsets.ViewSet):

    @swagger_auto_schema(
        operation_description="Update a Medicine",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Nome do medicamento."
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Descriçaõ do medicamento."
                ),
                "measurement_unit": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Unidade de medida.",
                    enum=[1, 2, 3, 4],
                ),  # G, MG, L, ML
                "presentation": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Tipo de apresentação.",
                    enum=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                ),  # PILLS, POWDER, etc.
                "batch_code": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Código de barras."
                ),
                "concentration": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Concentração."
                ),
                "therapeutic_class": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Classe terapêutica."
                ),
                "quantity": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Quantidade de itens."
                ),
            },
            required=[
                "quantity",
            ],
        ),
        responses={
            201: openapi.Response("Medicamento atualizado com sucesso!", MedicineSerializer)
        },
    )
    def update(self, request, pk=None):
        try:
            data = sanitize_data(request.data)
            if not data:
                raise ValidationError("Nenhum campo foi enviado no corpo da requisição.")
            with transaction.atomic():
                model_update = Medicine.objects.get(pk=pk)
                updated_model = MedicineSerializer(
                    model_update, data=data, partial=True
                )
                updated_model.is_valid(raise_exception=True)
                updated_model.save()
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Medicamento atualizado com sucesso!",
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