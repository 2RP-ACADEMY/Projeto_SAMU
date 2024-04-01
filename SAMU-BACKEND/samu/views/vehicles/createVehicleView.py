from rest_framework import viewsets
from rest_framework.response import Response
from samu.serializers.vehicleSerializer import VehicleSerializer
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from utils.string_helpers import sanitize_data


class CreateVehicleView(viewsets.ViewSet):

    def create(self, request):
        try:
            data = sanitize_data(request.data)
            vehicle = VehicleSerializer(
                data={
                    "available": True,
                    "name": data.get('name'),
                    "license_plate": data.get('license_plate')
                }
            )

            vehicle.is_valid(raise_exception=True)

            vehicle.save()
            
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Veículo criado com sucesso!", "object": vehicle.data, "code": 201}, status=201)

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