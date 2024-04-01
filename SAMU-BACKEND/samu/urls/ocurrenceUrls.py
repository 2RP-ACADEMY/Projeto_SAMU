from django.urls import path, include
from rest_framework.routers import DefaultRouter
from samu.views.ocurrence.masterOcurrenceView import MasterOcurrenceViewSet

router = DefaultRouter()
router.register('', MasterOcurrenceViewSet, basename="")

ocurrenceUrls = [
    path('', include(router.urls))
]