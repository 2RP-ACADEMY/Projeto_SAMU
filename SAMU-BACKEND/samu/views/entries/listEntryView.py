from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from ..requests.requestController import RequestController
from samu.serializers.entrySerializer import EntrySerializer, EntryFullSerializer
from samu.models.entryModel import Entry
from ..customFilters import filter_expiration_date_entry
from samu.pagination import StandardResultsSetPagination
from rest_framework.pagination import NotFound

class ListEntryView(viewsets.ViewSet):
    # Define the filter backends used for filtering and ordering the queryset.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['item__medicine__name', 'item__material__name', 'item__equipment__name']
    
    # Define the fields that can be used for ordering the queryset.
    ordering_fields = ['quantity', 'available_quantity', 'item__material__expiration_date', 'item__medicine__expiration_date', 'item__equipment__warranty_expire']

    # Define the fields that can be used for filtering the queryset.
    filterset_fields = {
        'item__type': ['exact', 'in'],
        'vehicle_id': ['exact', 'in', 'isnull'],
        'quantity': ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        'available_quantity': ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'],
        'date': ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte']
    }

    allowed_queries = ['expiration_date']

    def filter_queryset(self, queryset):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        # Return the filtered and ordered queryset.
        return queryset

    def list(self, request):
        try:
            after = self.request.query_params.get('af')
            before = self.request.query_params.get('bf')
            filtered_queryset = filter_expiration_date_entry(
                Entry.objects.all(), 
                after,
                "__gte"
            )
            filtered_queryset = filter_expiration_date_entry(
                filtered_queryset,
                before,
                "__lte"
            )
            filtered_queryset = self.filter_queryset(filtered_queryset)
            count_total = filtered_queryset.count()
            pagination = StandardResultsSetPagination()
            filtered_queryset = pagination.paginate_queryset(filtered_queryset, request)
            serializer_entries = EntryFullSerializer(filtered_queryset, many=True)

            if serializer_entries.data == []:
                RequestController.set_request_status(request_id=request.request_id, status_id=2)
                return Response({"detail": "Entradas não encontradas.", "total": count_total, "object": serializer_entries.data, "code": 200}, status=200)
            
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Entradas retornadas com  successo!", "total": count_total, "object": serializer_entries.data, "code": 200}, status=200)
        
        except NotFound as error:
            # Set the request status to indicate a permission error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 400}, status=403)
        
        except PermissionDenied as error:
            # Set the request status to indicate a permission error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 403}, status=403)
        
        except Exception as error:
            # Set the request status to indicate an internal server error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 500}, status=500)