from rest_framework import viewsets
from samu.views.users.createUserView import CreateUserView
from samu.views.users.getUserView import GetUserView
from samu.views.users.updateUserView import UpdateUserView
from samu.views.users.deleteUserView import DeleteUserView
from samu.views.users.listUserView import ListUserView
from samu.views.users.loginUserView import LoginUserView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated


# Define a master viewset that combines multiple user-related viewsets.
class MasterUserViewSet(
    CreateUserView,         # Inherits functionality for creating users.
    GetUserView,            # Inherits functionality for retrieving user details.
    UpdateUserView,         # Inherits functionality for updating users.
    DeleteUserView,         # Inherits functionality for deleting users.
    ListUserView,           # Inherits functionality for listing users with filters.
    LoginUserView
):
    
    # Define a mapping of view actions to the corresponding permission classes required for each action.
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'destroy': [IsAdminUser],
        'self_update': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'login': [IsAdminUser]
    }

    def get_permissions(self):
        # Returns a list of permission classes required for the current action.
        # Tries to retrieve permission classes specific to the current action using 'self.permission_classes_by_action',
        # and falls back to using the default permission classes defined in 'self.permission_classes' if not found.
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except:
            return [permission() for permission in self.permission_classes]