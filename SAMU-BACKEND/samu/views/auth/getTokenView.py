from drf_yasg.utils import swagger_auto_schema
from ...swagger_schemas.login.loginRequestSchema import body_login
from ...swagger_schemas.errors.errorSchema import errorSchema
from ...swagger_schemas.login.successfulLogin import successful_login
from ...swagger_schemas.login.loginBadRequestSchema import login_bad_request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from samu.views.requests.requestController import RequestController
from samu.models.userModel import User
from base64 import urlsafe_b64encode
from django.contrib.auth import authenticate, user_logged_in
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import PermissionDenied
from rest_authtoken.models import AuthToken
from utils.string_helpers import sanitize_data


class GetTokenView(ViewSet):
    @swagger_auto_schema(
        request_body=body_login,
        responses={200: successful_login, 400: login_bad_request, 500: errorSchema},
        tags=["Auth"],
    )
    def create(self, request: Request) -> Response:
        try:
            data = sanitize_data(request.data)

            try:
                user = User.objects.get(username=data.get('username'))
            except User.DoesNotExist:
                RequestController.set_request_status(
                    request_id=request.request_id, status_id=3
                )
                return Response({"detail": "Credênciais invalidas.", "code": 401}, status=401)

            # Check staff status
            if not user.is_staff:
                raise PermissionDenied(
                    "Você não tem acesso à esse endpoint."
                )

            # Then try to authenticate the user using the provided username and password.
            user = authenticate(username=user, password=data.get('password'))

            # Check if authentication was successful.
            if not user:
                RequestController.set_request_status(
                    request_id=request.request_id, status_id=3
                )
                return Response({"detail": "Credênciais invalidas."}, status=401)

            # If user is authenticated, delete existing tokens.
            AuthToken.objects.filter(user=user.id).delete()

            # Create an authentication token for the user.
            token = AuthToken.create_token_for_user(user)

            data = {
                "token": urlsafe_b64encode(token),
                "code": 201
            }

            user_logged_in.send(sender=user.__class__, request=request, user=user)
            RequestController.set_request_status(
                request_id=request.request_id, status_id=2
            )

            return Response(data)

        except PermissionDenied as error:
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

        except ValidationError as error:
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

        except Exception as error:
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
