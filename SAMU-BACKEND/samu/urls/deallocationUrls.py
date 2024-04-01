from django.urls import path, include
from rest_framework.routers import DefaultRouter
from samu.views.deallocation.createDeallocationView import CreateDeallocationView

router = DefaultRouter()
router.register('', CreateDeallocationView, basename="")

deallocationUrls = [
    path('', include(router.urls))
]