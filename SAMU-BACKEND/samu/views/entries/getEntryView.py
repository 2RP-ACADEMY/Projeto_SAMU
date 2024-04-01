from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from samu.models.entryModel import Entry
from samu.serializers.entrySerializer import EntrySerializer
from samu.views.requests.requestController import RequestController
from rest_framework.exceptions import PermissionDenied

class GetEntryView(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            with transaction.atomic():
                entry = Entry.objects.get(pk=pk)
                entry_data =  EntrySerializer(entry)

            RequestController.set_request_status(request_id=request.request_id, status_id=2)    
            return Response({"detail": "Entrada retornada com sucesso!", "object": entry_data.data, "code": 200}, status=200)
        
        except Entry.DoesNotExist as error:
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