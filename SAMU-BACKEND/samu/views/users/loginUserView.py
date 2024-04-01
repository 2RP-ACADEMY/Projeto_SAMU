from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.userModel import User
from ...serializers.userSerializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from ...swagger_schemas.users.userUniqueSchema import userUniqueSchema
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.errors.errorSchema401 import errorSchema401
from rest_framework.serializers import ValidationError
from ..requests.requestController import RequestController
from django.contrib.auth import authenticate
from samu.swagger_schemas.login.loginRequestSchema import body_login
from rest_framework.decorators import action

class LoginUserView(viewsets.ViewSet):
    # Define the query set to retrieve all users.
    queryset = User.objects.all()
    # Define the serializer class to serialize/deserialize user data.
    serializer_class = UserSerializer

    @swagger_auto_schema(
        request_body=body_login,
        responses={201: userUniqueSchema, 400: errorSchema, 401: errorSchema401},
        # Define the response codes and corresponding Swagger documentation schemas.
        tags=["User"]
        # Define the tags or categories to which this operation belongs in the documentation.
    )
    # Configure documentation with Swagger using the @swagger_auto_schema decorator.
    @action(methods=['post'], detail=False)
    def login(self, request):
        """
        Create a new user.

        Receives the instance and HTTP request as parameters.

        :param request: The HTTP request.
        :body request: user table data.
        :return: A response with details about the result of user creation and the created user instance
        """
        try:
            # Retrieve the data from the HTTP request body and store it in the 'data' variable.
            data = request.data

            if not data:
                raise ValidationError("Nenhum campo foi enviado no corpo da requisição.")

            username = request.data.get('username')
            if not username:
                raise ValidationError("O campo username é requisitado.")
            
            password = request.data.get('password')
            if not password:
                raise ValidationError("O campo password é requisitado.")

            user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password'))
            
            if user:
                # Set the request status to successfully completed.
                RequestController.set_request_status(request_id=request.request_id, status_id=2)
                return Response({"detail": True, "code": 200}, status=200)
            else:
                RequestController.set_request_status(request_id=request.request_id, status_id=3)
                return Response({"detail": False, "code": 400}, status=400)
        
        except ValidationError as error:
            # Set the request status to validation error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 400}, status=400)
        
        except Exception as error:
            # Set the request status to internal server error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 500}, status=500)