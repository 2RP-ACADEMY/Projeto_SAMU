from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from samu.models import Medicine
from ...serializers import MedicineSerializer
from ...swagger_schemas.parameters import token_param
from ...swagger_schemas.users.userListSchema import userListSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from drf_yasg.utils import swagger_auto_schema
from ..requests.requestController import RequestController
from samu.serializers import EntrySerializer
from samu.models import Entry
from samu.models import Item
from samu.serializers import MedicineFullSerializer
from samu.pagination import StandardResultsSetPagination
from rest_framework.pagination import NotFound


class ListMedicineView(viewsets.ViewSet):
    serializer_class = MedicineSerializer
    full_serializer_class = MedicineFullSerializer
    queryset = Medicine.objects.all()

    # Define the filter backends used for filtering and ordering the queryset.
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # # Define the fields that can be used for ordering the queryset.
    ordering_fields = [
        "entries__quantity",
        "entries_available_quantity",
        "entries__date",
        "medicine__expiration_date",
        "medicine__id",
        "medicine__name",
        "medicine__created_at",
        "medicine__therapeutic_class"
    ]

    # # Define the fields that can be used for searching the queryset.
    search_fields = [
        "medicine__name", 
        "medicine__description", 
        "medicine__batch_code",
    ]

    # # Define the fields that can be used for filtering the queryset.
    filterset_fields = {
        "entries__vehicle_id": ['exact', 'in', 'isnull'],
        "medicine__measurement_unit": ['exact', 'in'],
        "medicine__presentation": ['exact', 'in'],
        "entries__date": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        "entries__quantity": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        "entries__available_quantity": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        "medicine__expiration_date": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        "medicine__created_at": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte']
    }

    def filter_queryset(self, queryset):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        # Return the filtered and ordered queryset.
        return queryset

    def list(self, request):
        try:
            filtered_queryset = self.filter_queryset(Item.objects.all())
            count_total = filtered_queryset.count()
            pagination = StandardResultsSetPagination()
            filtered_queryset = pagination.paginate_queryset(filtered_queryset, request)
            serializer_entries = self.full_serializer_class(
                filtered_queryset, many=True
            )

            if serializer_entries.data == []:
                RequestController.set_request_status(
                    request_id=request.request_id, status_id=2
                )
                return Response(
                    {
                        "detail": "Medicamentos não encontrados",
                        "total": count_total,
                        "object": serializer_entries.data,
                        "code": 200
                    },
                    status=200,
                )

            filtered_data = [
                entry for entry in serializer_entries.data if entry.get("medicine")
            ]

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Medicamentos encontrados com sucesso!",
                    "total": count_total,
                    "object": filtered_data,
                    "code": 200
                },
                status=200,
            )

        except NotFound as error:
            # Set the request status to indicate a permission error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 400}, status=403)

        
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
