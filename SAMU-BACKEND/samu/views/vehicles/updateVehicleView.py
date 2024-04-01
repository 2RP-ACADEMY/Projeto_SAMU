from rest_framework import viewsets
from rest_framework.response import Response
from samu.models.vehicleModel import Vehicle
from samu.serializers.vehicleSerializer import VehicleSerializer
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from utils.string_helpers import sanitize_data

class UpdateVehicleView(viewsets.ViewSet):
    def update(self, request, pk=None):
        try:
            data = sanitize_data(request.data)
            
            vehicle = Vehicle.objects.get(pk=pk)

            updated_vehicle = VehicleSerializer(vehicle, data=data, partial=True)
            
            updated_vehicle.is_valid(raise_exception=True)
            updated_vehicle.save()

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Veículo atualizado com sucesso!", "object": updated_vehicle.data, "code": 201}, status=201)

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

        except Vehicle.DoesNotExist as error:
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