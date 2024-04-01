from django.urls import path, include
from rest_framework.routers import DefaultRouter
from samu.views.vehicles.masterVehicleView import MasterVehicleViewSet

router = DefaultRouter()
router.register('', MasterVehicleViewSet, basename="")

vehicleUrls = [
    path('', include(router.urls))
]