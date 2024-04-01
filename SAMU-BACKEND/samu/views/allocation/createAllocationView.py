from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from ..withdrawns.withdrawnController import WithdrawnController
from samu.views.entries.createEntryView import CreateEntryView
from samu.views.entries.updateEntryView import UpdateEntryView
from samu.models.entryModel import Entry
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied
from samu.serializers.entrySerializer import EntrySerializer
from utils.string_helpers import sanitize_data

class CreateAllocationView(viewsets.ViewSet):
    def create(self, request):
        try:
            data = sanitize_data(request.data)

            vehicle_id = data.get('vehicle_id')
            if vehicle_id == None:
                raise ValidationError('O campo vehicle_id é requisitado.')

            with transaction.atomic():
                entry = Entry.objects.get(pk=data.get("entry_id"))

                # raise exception if the entry_id is an allocated entry
                if entry.vehicle_id != None:
                    raise ValidationError('Não é possível alocar um registro de entrada já alocado.')
                
                withdrawn = WithdrawnController.create(
                    entry=entry, quantity=data.get("quantity"), reason=5
                )
                vehicle_entry = Entry.objects.filter(item=entry.item.id).filter(
                    vehicle_id=data.get("vehicle_id")
                )
                if vehicle_entry.exists():
                    UpdateEntryView.increase_quantity(
                        quantity=data.get("quantity"), pk=vehicle_entry[0].id
                    )
                    serialized_entry = EntrySerializer(vehicle_entry, many=True).data
                else:
                    serialized_entry = CreateEntryView.create(
                        item_id=entry.item.id, quantity=data.get("quantity")
                    )
                    serialized_entry = UpdateEntryView.set_vehicle(
                        vehicle_id=data.get("vehicle_id"), entry_id=serialized_entry["id"]
                    )

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response(
                {"detail": "Alocação criada com sucesso!", "object": serialized_entry, "code": 201}, status=201
            )
        
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
    
