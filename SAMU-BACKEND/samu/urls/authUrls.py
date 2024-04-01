from django.urls import path
from ..views.auth.getTokenView import GetTokenView


authUrls = [
    path('login/', GetTokenView.as_view({'post': 'create'}))
]