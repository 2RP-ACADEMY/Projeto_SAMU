from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from ..withdrawns.withdrawnController import WithdrawnController
from samu.views.entries.updateEntryView import UpdateEntryView
from samu.models.entryModel import Entry
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from samu.views.requests.requestController import RequestController
from samu.serializers.entrySerializer import EntrySerializer
from utils.string_helpers import sanitize_data


class CreateDeallocationView(viewsets.ViewSet):

    def create(self, request):
        try:
            data = sanitize_data(request.data)

            with transaction.atomic():
                vehicle_entry = Entry.objects.get(pk=data.get('entry_id'))
                if vehicle_entry.vehicle_id == None:
                    raise ValidationError("Não é possível deslocar um item que ja esta no estoque.")
                
                WithdrawnController.create(
                    entry=vehicle_entry,
                    quantity=data.get('quantity'),
                    reason=6
                )

                entry = Entry.objects.filter(item=vehicle_entry.item).filter(vehicle_id=None)
                
                UpdateEntryView.update_available_quantity(
                    quantity=data.get('quantity'),
                    entry=entry[0],
                    vehicle_entry=vehicle_entry
                )

                serialized_entry = EntrySerializer(entry[0]).data

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({"detail": "Deslocação realizada com sucesso!", "object": serialized_entry, "code": 201}, status=201)
        
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