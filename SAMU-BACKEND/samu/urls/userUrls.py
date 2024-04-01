from django.urls import path, include
from rest_framework.routers import DefaultRouter
from samu.views.users.masterUserView import MasterUserViewSet

route = DefaultRouter()
route.register('', MasterUserViewSet)

userUrls = [
    path('', include(route.urls))
]