from ...models.requestModel import Request
from ...serializers.requestSerializer import RequestSerializer

class RequestController():
    @staticmethod
    def create_request():
        """
        Create and return a request record.

        This function creates a new request record with an initial status and returns its ID.

        :return: ID of the created request.
        """
        # Create a new request record with an initial status_id of 1.
        request = RequestSerializer(data={"status_id": 1})

        # Validate the new request data, raising an exception if validation fails.
        request.is_valid(raise_exception=True)

        # Save the new request data to the database.
        request.save()

        # Retrieve the newly created request data based on its ID.
        request_data = Request.objects.get(pk=request.data['id'])

        # Return the ID of the newly created request.
        return request_data.id

    @staticmethod
    def set_request_type(request_id: int, type_id: int):
        """
        Define the request type and return the request record.

        :param request_id: The ID of the request.
        :param type_id: The ID of the request type.
        :return: Updated request data.
        """
        # Retrieve the request data based on the provided request_id.
        request_data = Request.objects.get(pk=request_id)

        # Create a new request serializer instance with updated type_id data and partial=True to allow partial updates.
        request = RequestSerializer(request_data, data={"type_id": type_id}, partial=True)

        # Validate the updated request data, raising an exception if validation fails.
        request.is_valid(raise_exception=True)

        # Save the updated request data.
        request.save()

        # Return the updated request data.
        return request.data

    @staticmethod
    def set_request_user(request_id: int, user_id: int):
        """
        Define the user associated with the request and return the request record.

        :param request_id: The ID of the request.
        :param user_id: The ID of the user associated with the request.
        :return: Updated request data.
        """
        # Retrieve the request data based on the provided request_id.
        request_data = Request.objects.get(pk=request_id)

        # Create a new request serializer instance with updated user_id data and partial=True to allow partial updates.
        request = RequestSerializer(request_data, data={"user_id": user_id}, partial=True)

        # Validate the updated request data, raising an exception if validation fails.
        request.is_valid(raise_exception=True)

        # Save the updated request data.
        request.save()

        # Return the updated request data.
        return request.data

    @staticmethod
    def set_request_status(request_id: int, status_id: int):
        """
        Define the status of the request and return the request record.

        :param request_id: The ID of the request.
        :param status_id: The ID of the request status.
        :return: Updated request data.
        """
        # Retrieve the request data based on the provided request_id.
        request_data = Request.objects.get(pk=request_id)

        # Create a new request serializer instance with updated status_id data and partial=True to allow partial updates.
        request = RequestSerializer(request_data, data={"status_id": status_id}, partial=True)

        # Validate the updated request data, raising an exception if validation fails.
        request.is_valid(raise_exception=True)

        # Save the updated request data.
        request.save()

        # Return the updated request data.
        return request.data