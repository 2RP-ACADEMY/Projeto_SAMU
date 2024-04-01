from rest_framework.permissions import IsAdminUser
from .getVehicleView import GetVehicleView
from .listVehicleView import ListVehicleView
from .createVehicleView import CreateVehicleView
from  .deleteVehicleView import DeleteVehicleView
from .updateVehicleView import UpdateVehicleView

# Define a master viewset that combines multiple user-related viewsets.
class MasterVehicleViewSet(
    CreateVehicleView,
    ListVehicleView,
    GetVehicleView,
    DeleteVehicleView,
    UpdateVehicleView
):
    # Define a mapping of view actions to the corresponding permission classes required for each action.
    permission_classes_by_action = {
        "create": [IsAdminUser], 
        "list": [IsAdminUser],
        "retrieve": [IsAdminUser],
        "destroy": [IsAdminUser],
        "update": [IsAdminUser]
    }

    def get_permissions(self):
        # Returns a list of permission classes required for the current action.
        # Tries to retrieve permission classes specific to the current action using 'self.permission_classes_by_action',
        # and falls back to using the default permission classes defined in 'self.permission_classes' if not found.
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except:
            return [permission() for permission in self.permission_classes]
