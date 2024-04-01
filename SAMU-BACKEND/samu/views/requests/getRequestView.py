from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.requestModel import Request
from ...serializers.requestSerializer import RequestSerializer
from ..requests.requestController import RequestController
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied

class GetRequestView(viewsets.ViewSet):
    # Define the query set to retrieve all requests.
    queryset = Request.objects.all()
    # Define the serializer class to serialize/deserialize request data.
    serializer_class = RequestSerializer

    
    # Configure Swagger documentation for this API endpoint.
    # - Assign the endpoint to the 'Request' category in Swagger tags.
    @swagger_auto_schema( tags=['Request'])
    def retrieve(self, request, pk=None):
        """
        Retrieves details of a specific request.

        :param request: The HTTP request.
        :param pk: The primary key of the request to be retrieved.
        :return: A response indicating the result of retrieving the request and the instance of the request.
        """
        try:
            # Retrieve the request data from the queryset based on the provided primary key (pk).
            request_data = self.queryset.get(pk=pk)

            # Create an instance of the RequestSerializer to serialize the request data.
            serializer = self.serializer_class(request_data)

            # Set the request status to indicate successful retrieval.
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Solicitação retornada com sucesso!", "object": serializer.data, "code": 200}, status=200)
        
        except Request.DoesNotExist as error:
            # Set the request status to indicate a request not found error.
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