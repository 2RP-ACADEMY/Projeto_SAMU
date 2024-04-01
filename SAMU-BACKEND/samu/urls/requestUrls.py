from django.urls import path, include
from rest_framework.routers import DefaultRouter
from samu.views.requests.masterRequestView import MasterRequestView

route = DefaultRouter()
route.register('', MasterRequestView)

requestUrls = [
    path('', include(route.urls))
]