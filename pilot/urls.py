from django.urls import path

from .views import CharacterView, OverviewView, callback

urlpatterns = [
    path("overview/", OverviewView.as_view(), name="overview"),
    path("callback/", callback, name="callback"),
    path("character/<uuid:pk>/", CharacterView.as_view(), name="character"),
]
