from rest_framework import viewsets
from samu.serializers import MedicineSerializer
from rest_framework.response import Response
from django.db import transaction
from samu.serializers import MedicineFullSerializer
from samu.models import Item
from samu.models import Medicine
from samu.views.requests.requestController import RequestController
from rest_framework.exceptions import PermissionDenied

class GetMedicineView(viewsets.ViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    full_serializer_class = MedicineFullSerializer

    def retrieve(self, request, pk=None):
        try:
            with transaction.atomic():
                item = Item.objects.get(pk=pk)
                model_data = self.full_serializer_class(item)

            if model_data.data.get("medicine") is None:
                RequestController.set_request_status(
                    request_id=request.request_id, status_id=3
                )
                return Response(
                    {
                        "detail": "O medicamento requisitado não existe na base de dados.",
                        "code": 404
                    },
                    status=404,
                )
            
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Medicamento encontrado com sucesso!",
                    "object": model_data.data,
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
                        "error_cause": error.args
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
