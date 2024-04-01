from django.urls import path, include
from rest_framework.routers import SimpleRouter
from samu.views.medicines.masterMedicineView import MasterMedicineViewSet

route = SimpleRouter()
route.register("", MasterMedicineViewSet)

medicineUrls = [
    path("", include(route.urls)),
]
