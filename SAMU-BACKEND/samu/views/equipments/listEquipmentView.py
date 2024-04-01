from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from samu.models.equipmentModel import Equipment
from ...serializers.materialSerializer import MaterialSerializer
from ...swagger_schemas.parameters import token_param
from ...swagger_schemas.users.userListSchema import userListSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from drf_yasg.utils import swagger_auto_schema
from ..requests.requestController import RequestController
from samu.serializers.entrySerializer import EntrySerializer
from samu.models.entryModel import Entry
from samu.models.itemModel import Item
from samu.serializers.equipmentSerializer import EquipmentFullSerializer
from samu.pagination import StandardResultsSetPagination
from rest_framework.pagination import NotFound


class ListEquipmentView(viewsets.ViewSet):
    # Define the filter backends used for filtering and ordering the queryset.
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # # Define the fields that can be used for ordering the queryset.
    ordering_fields = [
        "entries__quantity",
        "entries__available_quantity",
        "entries__date",
        "equipment__warranty_expire",
        "equipment__id"
    ]

    # # Define the fields that can be used for searching the queryset.
    search_fields = [
        "equipment__name",
        "equipment__description",
        "equipment__patrimony",
    ]

    # # Define the fields that can be used for filtering the queryset.
    filterset_fields = {
        "equipment__allocable": ['exact'],
        "entries__vehicle_id": ['exact', 'isnull', 'in'],
        "entries__date": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        "equipment__warranty_expire": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte', 'isnull'],
        "equipment__available": ['exact'],
        "entries__quantity": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        "entries__available_quantity": ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
    }

    

    def filter_queryset(self, queryset):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        # Return the filtered and ordered queryset.
        return queryset

    def list(self, request):
        try:
            filtered_queryset = self.filter_queryset(Item.objects.all()).exclude(
                equipment__isnull=True
            )
            count_total = filtered_queryset.count()
            pagination = StandardResultsSetPagination()
            filtered_queryset = pagination.paginate_queryset(filtered_queryset, request)
            serializer_entries = EquipmentFullSerializer(filtered_queryset, many=True)

            if serializer_entries.data == []:
                RequestController.set_request_status(
                    request_id=request.request_id, status_id=2
                )
                return Response(
                    {
                        "detail": "Equipamentos não encontrados.",
                        "total": count_total,
                        "object": serializer_entries.data,
                        "code": 200
                    },
                    status=200,
                )
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {
                    "detail": "Equipamentos encontrados com sucesso!",
                    "total": count_total,
                    "object": serializer_entries.data,
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
