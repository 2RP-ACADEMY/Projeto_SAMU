from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.userModel import User
from ...serializers.userSerializer import UserSerializer
from ...swagger_schemas.users.userUniqueSchema import userUniqueSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from drf_yasg.utils import swagger_auto_schema
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import PermissionDenied
from ..requests.requestController import RequestController
from utils.string_helpers import sanitize_data

class UpdateUserView(viewsets.ViewSet):
    # Define the query set to retrieve all users.
    queryset = User.objects.all()
    # Define the serializer class to serialize/deserialize user data.
    serializer_class = UserSerializer

    # Configure documentation with Swagger using the @swagger_auto_schema decorator.
    @swagger_auto_schema(
        request_body=UserSerializer,
        # Define the Swagger documentation schema for the request body.
        responses={
            201: userUniqueSchema,
            401: errorSchema401,
            400: errorSchema,
            404: errorSchema,
        },
        # Define the response codes and corresponding Swagger documentation schemas.
        tags=["User"]
        # Define the tags or categories to which this operation belongs in the documentation.
    )
    # Configure documentation with Swagger using the @swagger_auto_schema decorator.
    def update(self, request, pk=None):
        """
        Updates details of an existing user.

        Receives as parameters the instance, HTTP request, and user's primary key.

        :param request: The HTTP request.
        :param pk: The primary key of the user to be updated.
        :return: A response indicating the result of the user update, and updated user instance.
        """
        try:
            # Retrieve the data sent in the HTTP request body, which contains the updated user fields.
            updated_fields = sanitize_data(request.data)

            if not updated_fields:
                # If no fields are being sent in the request body, raise a validation error.
                raise ValidationError("Nenhum campo foi enviado no corpo da requisição.")

            if "password" in updated_fields:
                # If 'password' is in the updated fields, hash the new password.
                updated_fields["password"] = make_password(updated_fields["password"])

            # Retrieve the user instance to be updated using the provided primary key (pk).
            updated_user = self.queryset.get(pk=pk)

            # Create an instance of the UserSerializer to update the user's data.
            # Use the 'data' parameter to provide the updated fields from the request.
            # 'partial=True' allows partial updates of the user's data (not all fields are required).
            serializer = self.serializer_class(
                updated_user, data=updated_fields, partial=True
            )

            # Validate the serializer data, raising an exception if it's not valid.
            serializer.is_valid(raise_exception=True)

            # Save the changes to the user's data as specified in the serializer.
            serializer.save()

            # Set the request status to successfully completed.
            RequestController.set_request_status(
                request_id=request.request_id, status_id=2
            )
            return Response(
                {"detail": "Usuário atualizado com sucesso!", "object": serializer.data, "code": 201},
                status=201
            )

        except ValidationError as error:
            # Set the request status to validation error.
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
                    "code": 400
                },
                status=400,
            )

        except User.DoesNotExist as error:
            # Set the request status to indicate a user not found error.
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
