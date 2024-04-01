from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.ocurrenceModel import Ocurrence
from samu.serializers.ocurrenceSerializer import OcurrenceSerializer
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from utils.string_helpers import sanitize_data
from datetime import timezone
from django.utils import timezone

class UpdateOcurrenceView(viewsets.ViewSet):
    def update(self, request, pk=None):
        try:

            # Remove spaces at the beginning and end data received in the request
            data = sanitize_data(request.data)

            end_datetime = data.get('end_datetime')

            # Retrieve the Ocurrence object with the specified primary key (pk)
            ocurrence = Ocurrence.objects.get(pk=pk)
            
            # Create an OcurrenceSerializer instance with the existing Ocurrence object
            # Update the 'end_datetime' field with the new value if provided, or use the current time
            updated_ocurrence = OcurrenceSerializer(ocurrence, data={"end_datetime": end_datetime if end_datetime else timezone.now()}, partial=True)
            
            # Validate the OcurrenceSerializer instance
            ocurrence.is_valid(raise_exception=True)

            # Save the ocurrence
            ocurrence.save()

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Ocorrência atualizada com sucesso!", "object": updated_ocurrence.data, "code": 201}, status=201)

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

        except Ocurrence.DoesNotExist as error:
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