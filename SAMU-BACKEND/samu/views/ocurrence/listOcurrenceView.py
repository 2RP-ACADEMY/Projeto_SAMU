from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from ..requests.requestController import RequestController
from samu.serializers.ocurrenceSerializer import OcurrenceSerializer
from samu.models.ocurrenceModel import Ocurrence
from rest_framework import filters
from samu.pagination import StandardResultsSetPagination
from rest_framework.pagination import NotFound

class ListOcurrenceView(viewsets.ViewSet):

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    # Define the fields that can be used for ordering the queryset.
    ordering_fields = [
        "id",
        "start_datetime",
        "end_datetime"
    ]

    # Define the fields that can be used for searching the queryset.
    search_fields = [
        "id"
    ]

    def filter_queryset(self, queryset):
        """
        Filters and orders the queryset based on specified filters and ordering.

        :param queryset: The queryset to be filtered and ordered.
        :return: A filtered and sorted queryset.
        """

        # Apply each filter backend in the list of filter backends to filter and order the queryset.
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        # Return the filtered and ordered queryset.
        return queryset
    
    def list(self, request):
        try:
            # Get list of all ocurrences
            filtered_queryset = self.filter_queryset(Ocurrence.objects.all())
            count_total = filtered_queryset.count()
            pagination = StandardResultsSetPagination()
            filtered_queryset = pagination.paginate_queryset(filtered_queryset, request)
            # Serialize the filtered queryset into a list of dictionary entries
            serializer_entries = OcurrenceSerializer(filtered_queryset, many=True)

            # Check if the serialized data is empty, to change returned message
            if serializer_entries.data == []:
                RequestController.set_request_status(request_id=request.request_id, status_id=2)
                return Response({"detail": "Ocorrências não encontrados", "total": count_total, "object": serializer_entries.data, "code": 200}, status=200)
            
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Ocorrências retornados com sucesso!", "total": count_total , "object": serializer_entries.data, "code": 200}, status=200)
        
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