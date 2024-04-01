from rest_framework import viewsets
from datetime import date, datetime
from samu.models import Medicine
from samu.serializers import MedicineSerializer
from samu.serializers.medicineSerializer import MedicineFullSerializer
from rest_framework.response import Response
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from ..items.createItemView import CreateItemView
from ..entries.createEntryView import CreateEntryView
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from utils.string_helpers import sanitize_data


class CreateMedicineView(viewsets.ViewSet):
    queryset_create = Medicine.objects.all()
    serializer_class_create = MedicineSerializer

    def validate_request_fields(self, data):
        required_fields = [
            "name",
            "measurement_unit",
            "presentation",
            "batch_code",
            "concentration",
            "therapeutic_class",
        ]
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"{field} é um campo obrigatório.")

        for field in ["measurement_unit", "presentation"]:
            if field in data and isinstance(data[field], str) and data[field].isdigit():
                data[field] = int(data[field])

    @swagger_auto_schema(
        operation_description="Cadastrar novo medicamento.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Nome do medicamento."
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Descrição do medicamento."
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
                "name",
                "measurement_unit",
                "presentation",
                "batch_code",
                "concentration",
                "therapeutic_class",
            ],
        ),
        responses={201: openapi.Response("Medicamento cadastrado com sucesso!", MedicineSerializer)},
    )
    def create(self, request):
        try:
            data = sanitize_data(request.data)
            if not data:
                raise ValidationError('Nenhum campo foi enviado no corpo da requisição.')

            self.validate_request_fields(data)
            
            expiration_date = data.get("expiration_date")
            # Check and convert the expiration date to datetime.date
            expiration_date_str = data.get("expiration_date")
            if expiration_date_str:
                expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
                if expiration_date < date.today():
                    raise ValidationError('A data de validade não pode ser anterior do que a data atual.')

            with transaction.atomic():
                item = CreateItemView.create(item_type=1, item_conception=request.data.get('item_conception'))
                medicine = self.serializer_class_create(
                    data={
                        "id": item.id,
                        "name": data.get('name'),
                        "description": data.get("description"),
                        "measurement_unit": data.get("measurement_unit"),
                        "presentation": data.get("presentation"),
                        "batch_code": data.get("batch_code"),
                        "concentration": data.get("concentration"),
                        "therapeutic_class": data.get("therapeutic_class"),
                        "expiration_date": expiration_date if expiration_date_str else None  # Use the converted expiration date
                    }
                )
                medicine.is_valid(raise_exception=True)
                medicine.save()
                entry = CreateEntryView.create(
                    item_id=item.id,
                    quantity=data.get("quantity"),
                )
                medicine_data = MedicineFullSerializer(item)

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {"detail": "Medicamento cadastrado com sucesso!", "object": medicine_data.data, "code": 201},
                status=status.HTTP_201_CREATED,
            )
        
        except (ValidationError, KeyError) as error:
            # Set the request status to validation error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 400}, status=400)

        except PermissionDenied as error:
            # Set the request status to permission error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 403}, status=403)

        except Exception as error:
            # Set the request status to internal server error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 500}, status=500)
