from django.urls import path, include
from rest_framework.routers import DefaultRouter
from samu.views.allocation.createAllocationView import CreateAllocationView

router = DefaultRouter()
router.register('', CreateAllocationView, basename="")

allocationUrls = [
    path('', include(router.urls))
]