from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.userModel import User
from ...serializers.userSerializer import UserSerializer
from ...swagger_schemas.parameters import token_param
from ...swagger_schemas.users.userUniqueSchema import userUniqueSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from ..requests.requestController import RequestController

class GetUserView(viewsets.ViewSet):
    # Define the query set to retrieve all users.
    queryset = User.objects.all()
    # Define the serializer class to serialize/deserialize user data.
    serializer_class = UserSerializer

    @swagger_auto_schema(
        # Define the expected response codes and their corresponding Swagger documentation schemas.
        responses={200: userUniqueSchema, 401: errorSchema401, 400: errorSchema},
        # Define the tags or categories to which this operation belongs in the documentation.
        tags=["User"]
    )
    # Configure documentation with Swagger using the @swagger_auto_schema decorator.
    def retrieve(self, request, pk=None):
        """
        Retrieves details of a specific user.

        Receives as parameters the instance, HTTP request, and user's primary key.

        :param request: The HTTP request.
        :param pk: The primary key of the user to retrieve details for.
        :return: A response containing details of the requested user, including the user instance.
        """
        try:
            # Retrieve the user with the specified primary key.
            user = self.queryset.get(pk=pk)
            # Serialize the user's data using the serializer class.
            serializer = self.serializer_class(user)

            # Set the request status to successfully completed.
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            
            # Return a response with details of the requested user, including the user instance.
            return Response({"detail": "Usuário retornado com sucesso!", "object": serializer.data, "code": 200}, status=200)
        
        except User.DoesNotExist as error:
            # Set the request status to indicate a user not found error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 404}, status=404)
        
        except PermissionDenied as error:
            # Set the request status to indicate a permission error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 403}, status=403)
        
        except Exception as error:
            # Set the request status to indicate an internal server error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 500}, status=500)