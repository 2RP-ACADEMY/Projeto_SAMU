from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.userModel import User
from ...serializers.userSerializer import UserSerializer
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from ...swagger_schemas.parameters import token_param
from ...swagger_schemas.users.userUniqueSchema import userUniqueSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from ..requests.requestController import RequestController
from utils.string_helpers import sanitize_data

class CreateUserView(viewsets.ViewSet):
    # Define the query set to retrieve all users.
    queryset = User.objects.all()
    # Define the serializer class to serialize/deserialize user data.
    serializer_class = UserSerializer

    @swagger_auto_schema(
        request_body=UserSerializer,
        # Define the Swagger documentation schema for the request body.
        responses={201: userUniqueSchema, 400: errorSchema, 401: errorSchema401},
        # Define the response codes and corresponding Swagger documentation schemas.
        tags=["User"]
        # Define the tags or categories to which this operation belongs in the documentation.
    )
    # Configure documentation with Swagger using the @swagger_auto_schema decorator.
    def create(self, request):
        """
        Create a new user.

        Receives the instance and HTTP request as parameters.

        :param request: The HTTP request.
        :body request: user table data.
        :return: A response with details about the result of user creation and the created user instance
        """
        try:
            # Retrieve the data from the HTTP request body and store it in the 'data' variable.
            data = sanitize_data(request.data)

            # If no data is provided in the request body, raise a ValidationError indicating that no fields are being sent.
            if not data:
                raise ValidationError("Nenhum campo foi enviado no corpo da requisição.")

            # Encrypt the password before saving it to the database.
            data['password'] = make_password(data['password'])

            # Create a user instance using the defined serializer class and the provided data.
            user = self.serializer_class(data=data)

            # Check if the user data is valid according to the serializer's validation rules.
            user.is_valid(raise_exception=True)

            # Save the validated user data to the database.
            user.save()

            # Set the request status to successfully completed.
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            
            return Response({"detail": "Usuário criado com sucesso!", "object": user.data, "code": 201}, status=201)

        except KeyError as error:
            # Set the request status to validation error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': [{"password": ["Este campo é necessário."]}]}, "code": 400}, status=400)

        except ValidationError as error:
            # Set the request status to validation error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args, "code": 400}}, status=400)

        except PermissionDenied as error:
            # Set the request status to permission error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": { 'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 403}, status=403)

        except Exception as error:
            # Set the request status to internal server error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 500}, status=500)