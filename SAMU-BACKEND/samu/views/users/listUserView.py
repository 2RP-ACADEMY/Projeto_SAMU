from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from samu.models.userModel import User
from ...serializers.userSerializer import UserSerializer
from ...swagger_schemas.parameters import token_param
from ...swagger_schemas.users.userListSchema import userListSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from drf_yasg.utils import swagger_auto_schema
from ..requests.requestController import RequestController
from samu.pagination import StandardResultsSetPagination
from rest_framework.pagination import NotFound

class ListUserView(viewsets.ViewSet):
    # Define the query set to retrieve all users.
    
    queryset = User.objects.all()
    # Define the serializer class to serialize/deserialize user data.
    serializer_class = UserSerializer

    # Define the filter backends used for filtering and ordering the queryset.
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    # Define the fields that can be used for ordering the queryset.
    ordering_fields = ['name', 'username', 'id']

    # Define the fields that can be used for searching the queryset.
    search_fields = ['name', 'email', 'username']

    # Define the fields that can be used for filtering the queryset.
    filterset_fields = ['is_active', 'is_staff', 'is_superuser', 'is_deleted']

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
    
    @swagger_auto_schema(
        # Define the expected response codes and their corresponding Swagger documentation schemas.
        responses={200: userListSchema, 400: errorSchema, 401: errorSchema401},
        # Define the tags or categories to which this operation belongs in the documentation.
        tags=["User"]
    )
    # Configure documentation with Swagger using the @swagger_auto_schema decorator.
    def list(self, request):
        """
        Lists all users using filters.

        Receives as parameters the instance and HTTP request.

        :param request: The HTTP request.
        :return: A response containing a list of users and a success message.
        """
        try:
            # Filter and order the queryset based on specified filters and ordering.
            queryset = self.filter_queryset(self.queryset)
            count_total = queryset.count()
            pagination = StandardResultsSetPagination()
            queryset = pagination.paginate_queryset(queryset, request)
            # Serialize the user's data using the serializer class.
            serializer = self.serializer_class(queryset, many=True)
            
            # Check if the serialized data is an empty list, indicating that no users were found.
            if serializer.data == []:
                # Set the request status to successfully completed.
                RequestController.set_request_status(request_id=request.request_id, status_id=2)
                return Response({"detail": "Usuários não encontrados.", "object": serializer.data, "code": 200}, status=200)
            
            # Set the request status to successfully completed.
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Usuários retornados com sucesso!", "total":count_total, "object": serializer.data, "code": 200}, status=200)
        
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