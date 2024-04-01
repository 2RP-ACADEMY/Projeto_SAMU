from rest_framework import viewsets
from rest_framework.response import Response
from samu.serializers.vehicleSerializer import VehicleSerializer
from samu.models.vehicleModel import Vehicle
from ..requests.requestController import RequestController
from rest_framework.exceptions import PermissionDenied

class DeleteVehicleView(viewsets.ViewSet):
    
    def destroy(self, request, pk=None):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            print(vehicle)
            deleted_vehicle = VehicleSerializer(vehicle)
            print(deleted_vehicle.data)
            vehicle.delete()

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Veículo deletado com sucesso!", "object": deleted_vehicle.data, "code": 200}, status=200)
        
        except Vehicle.DoesNotExist as error:
            # Set the request status to indicate a user not found error.
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