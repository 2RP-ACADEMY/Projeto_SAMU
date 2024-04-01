from django.contrib import admin
from django.urls import path, include
from samu.urls.userUrls import userUrls
from samu.urls.authUrls import authUrls
from samu.urls.requestUrls import requestUrls
from samu.urls.materialUrls import materialUrls
from samu.urls.medicineUrls import medicineUrls
from samu.urls.equipmentUrls import equipmentUrls
from samu.urls.withdrawnUrls import withdrawnUrls
from samu.urls.vehicleUrls import vehicleUrls
from samu.urls.allocationUrls import allocationUrls
from samu.urls.deallocationUrls import deallocationUrls
from samu.urls.entryUrls import entryUrls
from samu.urls.ocurrenceUrls import ocurrenceUrls
from samu.urls.itemConceptionUrls import itemConceptionUrls

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="SAMU API",
        default_version="Beta",
        # description="Test description",
    ),
    public=True,
)

## api urls
urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include(userUrls)),
    path("auth/", include(authUrls)),
    path("requests/", include(requestUrls)),
    path("materials/", include(materialUrls)),
    path("medicines/", include(medicineUrls)),
    path("equipments/", include(equipmentUrls)),
    path("withdrawns/", include(withdrawnUrls)),
    path("vehicles/", include(vehicleUrls)),
    path("allocation/", include(allocationUrls)),
    path("deallocation/", include(deallocationUrls)),
    path("entries/", include(entryUrls)),
    path("ocurrences/", include(ocurrenceUrls)),
    path("itemconception/", include(itemConceptionUrls))
]

## documentation urls
urlpatterns += [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
