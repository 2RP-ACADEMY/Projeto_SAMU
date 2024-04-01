from samu.views.requests.requestController import RequestController
from django.http import JsonResponse
from .codesByUrlAndMethod import get_number_from_mapping
import json

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware for custom authentication and request logging.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """

        # Create a unique request ID and associate it with the request.
        request_id = RequestController.create_request()

        # Associate the request_id with the current HTTP request object.
        request.request_id = request_id
        
        # Process the request and obtain the response.
        response = self.get_response(request)
        
        # Determine the view code based on the URL and HTTP method.
        view_code = get_number_from_mapping(request.path, request.method)

        # If a view code is found, set the request type for the current request.
        if view_code:
            RequestController.set_request_type(request_id=request_id, type_id=view_code) 
        
        # Handle 404 (Page not found) errors.
        if response.status_code == 404:
            try:
                response_content = json.loads(response.content)
                if 'detail' in response_content.keys():
                    return response
            except:
                return self.handle_404(request)
        
        # Handle 405 (Method not allowed) errors.
        if response.status_code == 405:
            return self.handle_405(request)

        return response
    
    def handle_404(self, request):
        """
        Handle 404 (Page not found) errors.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating a 404 error.
        """
        RequestController.set_request_status(request_id=request.request_id, status_id=3)
        return JsonResponse({"detail": "Página não encontrada."}, status=404)
    
    def handle_405(self, request):
        """
        Handle 405 (Method not allowed) errors.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating a 405 error.
        """
        RequestController.set_request_status(request_id=request.request_id, status_id=3)
        return JsonResponse({"detail": f"Método {request.method} não permitido."}, status=405)



