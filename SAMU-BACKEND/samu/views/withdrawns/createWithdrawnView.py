from rest_framework import viewsets
from .withdrawnController import WithdrawnController
from rest_framework.response import Response
from django.db import transaction
from samu.models.entryModel import Entry
from ..requests.requestController import RequestController
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied

class CreateWithdrawnView(viewsets.ViewSet):

    def create(self, request):
        try:
            body = request.data

            with transaction.atomic():
                entry = Entry.objects.get(pk=body.get('entry_id'))
                withdrawn = WithdrawnController.create(
                    entry= entry,
                    quantity=body.get('quantity'),
                    reason=body.get('reason')
                )

            RequestController.set_request_status(request_id=request.request_id, status_id=2)
            return Response({'detail': "Saída registrada com sucesso!", 'object': withdrawn, "code": 201}, status=201)
        
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
