from rest_authtoken.auth import AuthTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from ..views.requests.requestController import RequestController

class AuthMiddleware(AuthTokenAuthentication):
    """   
        this class inherits from the authentication base class to add error handling
    """
    def authenticate(self, request):
        """
        Authenticate the HTTP request using the token authentication mechanism.

        
        :param request: The HTTP request.
        Returns:
            Tuple[User, Token]: A tuple containing the authenticated user object and the authentication token,
                                or None if authentication fails.
        """
        try:
            # Attempt to authenticate the request using the token-based authentication mechanism.
            response = super().authenticate(request)

            # If authentication fails or does not return a result, raise the NotAuthenticated exception.
            if not response:
                raise NotAuthenticated

            # Return the result of authentication (a tuple containing the authenticated user and the token).
            return response

        except NotAuthenticated as error:
            # Set the request status to 3 (indicating failure) and continue execution.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            pass

        except AuthenticationFailed as error:
            # Set the request status to 3 (indicating failure) and raise the AuthenticationFailed exception with a custom message.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            raise AuthenticationFailed('Token de acesso inválido.')

        except Exception as error:
            # Set the request status to 3 (indicating failure) in case of unhandled exception.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)