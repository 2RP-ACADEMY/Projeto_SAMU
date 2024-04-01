from django.urls import path, include
from rest_framework.routers import SimpleRouter
from samu.views.item_conception.masterItemConceptionView import MasterItemConceptionViewSet

route = SimpleRouter()
route.register("", MasterItemConceptionViewSet, basename="")

itemConceptionUrls = [
    path("", include(route.urls)),
]
