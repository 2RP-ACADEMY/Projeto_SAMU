from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters
from samu.models.requestModel import Request
from ...serializers.requestSerializer import RequestSerializer
from ..requests.requestController import RequestController
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from samu.pagination import StandardResultsSetPagination
from rest_framework.pagination import NotFound

class ListRequestView(viewsets.ViewSet):
    # Define the query set to retrieve all requests.
    queryset = Request.objects.all()
    # Define the serializer class to serialize/deserialize request data.
    serializer_class = RequestSerializer

    # Define filter backends to enable filtering and ordering.
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Specify fields for ordering the queryset.
    ordering_fields = ['id', 'created_at', 'status_id', 'type_id']

    # Specify fields for filtering the queryset.
    filterset_fields = {
        'created_at': ['exact', 'in', 'range', 'lt', 'lte', 'gt', 'gte'], 
        'status_id': ['exact', 'in'], 
        'type_id': ['exact', 'in']
                        
    }

    # Custom method to filter and order the queryset based on specified filters and ordering.
    def filter_queryset(self, queryset):
        """
        Filters and orders the queryset based on specified filters and ordering.

        :param queryset: The original queryset.
        :return: A filtered and sorted queryset.
        """
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    # Configure Swagger documentation for this API endpoint.
    # - Assign the endpoint to the 'Request' category in Swagger tags.
    @swagger_auto_schema( tags=['Request'])
    def list(self, request):
        """
        Lists all requests using specified filters and ordering.

        :param request: The HTTP request.
        :return: A response indicating the result of the request and the list of requests.
        """
        try:
            # Filter and order the queryset based on specified filters and ordering.
            queryset = self.filter_queryset(Request.objects.all())
            pagination = StandardResultsSetPagination()
            queryset = pagination.paginate_queryset(queryset, request)
            # Create a serializer instance to serialize the queryset with many=True, indicating multiple objects.
            serializer = self.serializer_class(queryset, many=True)

            if serializer.data == []:
                # Set the request status to indicate no requests found.
                RequestController.set_request_status(request_id=request.request_id, status_id=2)
                return Response({"detail": "Solicitações não encontradas.", "object": serializer.data, "code": 200}, status=200)
            
            # Set the request status to indicate successful request listing.
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Solicitações retornadas com sucesso!", "object": serializer.data, "code": 200}, status=200)
        
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