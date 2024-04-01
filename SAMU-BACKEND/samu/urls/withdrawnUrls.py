from django.urls import path, include
from rest_framework.routers import SimpleRouter
from samu.views.withdrawns.masterWithdrawnView import MasterWithdrawnViewSet

router = SimpleRouter()
router.register('', MasterWithdrawnViewSet, basename="")

withdrawnUrls = [
    path('', include(router.urls))
]