from django.urls import path, include
from rest_framework.routers import SimpleRouter
from samu.views.equipments.masterEquipmentViewSet import MasterEquipmentViewSet

route = SimpleRouter()
route.register("", MasterEquipmentViewSet)

equipmentUrls = [
    path("", include(route.urls)),
]
