from django.urls import path, include
from rest_framework.routers import DefaultRouter
from samu.views.entries.listEntryView import ListEntryView
from samu.views.entries.getEntryView import GetEntryView
from samu.views.entries.masterEntryView import MasterEntryView

router = DefaultRouter()
router.register('', MasterEntryView, basename="")

entryUrls = [
    path('', include(router.urls))
]