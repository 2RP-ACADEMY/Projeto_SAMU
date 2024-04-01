from django.urls import path, include
from rest_framework.routers import SimpleRouter
from samu.views.materials.masterMaterialView import MasterMaterialViewSet

route = SimpleRouter()
route.register('', MasterMaterialViewSet)

materialUrls = [
    path('', include(route.urls)),
]