from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from samu.models.itemModel import Item
from samu.views.requests.requestController import RequestController
from rest_framework.exceptions import PermissionDenied
from samu.serializers.materialSerializer import MaterialFullSerializer

class DeleteMaterialView(viewsets.ViewSet):

    def destroy(self, request, pk=None):
        try:
            with transaction.atomic():
                item = Item.objects.get(pk=pk)
                material = MaterialFullSerializer(item)
                material = material.data
                item.delete()
            
            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Material excluído com sucesso!", "object": material, "code": 201}, status=201)

        except Item.DoesNotExist as error:
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