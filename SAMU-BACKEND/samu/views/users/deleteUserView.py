from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.userModel import User
from ...serializers.userSerializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from ...swagger_schemas.parameters import token_param
from ...swagger_schemas.users.userUniqueSchema import userUniqueSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from rest_framework.exceptions import PermissionDenied
from ..requests.requestController import RequestController

class DeleteUserView(viewsets.ViewSet):
    # Define the query set to retrieve all users.
    queryset = User.objects.all()
    # Define the serializer class to serialize/deserialize user data.
    serializer_class = UserSerializer
    
    @swagger_auto_schema(
        # Define the expected response codes and their corresponding Swagger documentation schemas.
        responses={200: userUniqueSchema, 401: errorSchema401, 404: errorSchema},
        # Define the tags or categories to which this operation belongs in the documentation.
        tags=["User"]
    )
    # Configure documentation with Swagger using the @swagger_auto_schema decorator.
    def destroy(self, request, pk=None):
        """
        Deletes an existing user.

        Receives as parameters the instance, HTTP request, and user's primary key.

        :param request: The HTTP request.
        :param pk: The primary key of the user to be deleted.
        :return: A response indicating the result of the user deletion and the instance of deleted user.
        """
        try:
            # Retrieve the user with the specified primary key.
            deleted_user = self.queryset.get(pk=pk)

            # Create an instance of the UserSerializer to update the user's data.
            # Use the 'data' parameter to provide the updated fields from the request.
            # 'partial=True' allows partial updates of the user's data (not all fields are required).
            serializer = self.serializer_class(
                deleted_user, data={
                    "is_active": False,
                    "is_deleted": True
                }, partial=True
            )

            # Validate the serializer data, raising an exception if it's not valid.
            serializer.is_valid(raise_exception=True)

            # Save the changes to the user's data as specified in the serializer.
            serializer.save()
            
            # Set the request status to successfully completed.
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Usuário deletado com sucesso!", "object": serializer.data, "code": 200}, status=200)
        
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