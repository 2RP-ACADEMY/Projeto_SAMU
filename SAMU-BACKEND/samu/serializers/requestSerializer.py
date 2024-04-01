from rest_framework import serializers
from ..models.requestModel import Request, RequestType


class RequestSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source="type_id.name", read_only=True)
    status_name = serializers.CharField(source="status_id.name", read_only=True)

    class Meta:
        model = Request
        fields = [f.name for f in Request._meta.fields] + ["type_name", "status_name"]
