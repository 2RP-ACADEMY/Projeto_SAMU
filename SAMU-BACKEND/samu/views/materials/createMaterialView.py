from rest_framework import viewsets, status
from datetime import date, datetime
from samu.serializers.materialSerializer import MaterialSerializer
from rest_framework.response import Response
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from ..items.createItemView import CreateItemView
from ..entries.createEntryView import CreateEntryView
from django.db import transaction
from samu.serializers.materialSerializer import MaterialFullSerializer
from rest_framework.exceptions import PermissionDenied
from samu.models.itemConceptionModel import ItemConception
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
)


class CreateMaterialView(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=request_body,
        responses={201: "Material cadastrado com sucesso!"},
        operation_description="Cria um novo material.",
    )
    def create(self, request):
        try:
            data = sanitize_data(request.data)

            if not data:
                raise ValidationError('Nenhum campo foi enviado no corpo da requisição.')
            
            expiration_date = data.get("expiration_date")
            # Check and convert the expiration date to datetime.date
            expiration_date_str = data.get("expiration_date")
            if expiration_date_str:
                expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
                if expiration_date < date.today():
                    raise ValidationError('A data de validade não pode ser anterior do que a data atual.')
                
            with transaction.atomic():
                item = CreateItemView.create(item_type=2, item_conception=request.data.get('item_conception'))
                material = MaterialSerializer(
                    data={
                        "id": item.id,
                        "name": request.data.get("name"),
                        "description": request.data.get("description"),
                        "batch_code": request.data.get("batch_code"),
                        "allocable": request.data.get("allocable"),
                        "expiration_date": expiration_date if expiration_date_str else None  # Use the converted expiration date
                    }
                )
                material.is_valid(raise_exception=True)
                material.save()
                entry = CreateEntryView.create(
                    item_id=item.id, quantity=data.get("quantity")
                )
                material_data = MaterialFullSerializer(item)

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Material cadastrado com sucesso!",
                    "object": material_data.data,
                    "code": 201
                },
                status=201,
            )

        except (ValidationError, KeyError) as error:
            # Set the request status to validation error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 400}, status=400)
        
        except PermissionDenied as error:
            # Set the request status to permission error.
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
            # Set the request status to internal server error.
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
