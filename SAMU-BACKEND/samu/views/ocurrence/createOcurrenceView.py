from rest_framework import viewsets
from rest_framework.response import Response
from samu.serializers.ocurrenceSerializer import OcurrenceSerializer
from samu.models.vehicleModel import Vehicle
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from utils.string_helpers import sanitize_data
from django.utils import timezone

class CreateOcurrenceView(viewsets.ViewSet):

    def create(self, request):
        try:

            # Remove spaces at the beginning and end data received in the request
            data = sanitize_data(request.data)
            vehicle = data.get('vehicle_id')
            start_datetime = data.get('start_datetime')

            # Create an OcurrenceSerializer instance with the provided data
            # If 'start_datetime' is not provided, use the current time
            ocurrence = OcurrenceSerializer(
                data={
                
                    "vehicle": vehicle,
                    "start_datetime": start_datetime if start_datetime else timezone.now()
                }
            )

            # Validate the OcurrenceSerializer instance
            ocurrence.is_valid(raise_exception=True)

            # Save the ocurrence
            ocurrence.save()
            
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Ocorrência criado com sucesso!", "object": ocurrence.data, "code": 201}, status=201)

        except (ValidationError, KeyError) as error:
            # Set the request status to validation error.
            # Set the request status to indicate failure (status_id=3) using the RequestController.
            RequestController.set_request_status(request_id=request.request_id, status_id=3)
            return Response({"detail": {'error_name': error.__class__.__name__, 'error_cause': error.args}, "code": 400}, status=400)

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