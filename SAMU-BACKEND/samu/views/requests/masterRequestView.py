from .listRequestsView import ListRequestView
from .getRequestView import GetRequestView
from rest_framework.permissions import IsAdminUser

class MasterRequestView(
    ListRequestView,
    GetRequestView
): 
    # Define permission classes based on the current action.
    permission_classes_by_action = {
        'list': [IsAdminUser],     # Permission required for listing requests.
        'retrieve': [IsAdminUser], # Permission required for retrieving a single request.
    }

    def get_permissions(self):
        """
        Returns a list of permission classes required for the current action.

        If a specific permission class is defined for the current action in
        'permission_classes_by_action', it will be used. Otherwise, the default
        permission classes from 'permission_classes' will be used.

        :return: List of permission classes.
        """
        try:
            # Use the defined permission classes for the current action, if available.
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # If no specific permission is defined, use the default permission classes.
            return [permission() for permission in self.permission_classes]
