from django.urls import path

from .views import (ArticleView, CategoryView, ConstellationView, GroupView,
                    RegionView, SystemView, UniverseView)

urlpatterns = [
    path("article/<int:pk>/", ArticleView.as_view(), name="article"),
    path("category/<int:pk>/", CategoryView.as_view(), name="category"),
    path("group/<int:pk>/", GroupView.as_view(), name="group"),
    path("system/<int:pk>/", SystemView.as_view(), name="system"),
    path("constellation/<int:pk>/", ConstellationView.as_view(), name="constellation"),
    path("region/<int:pk>/", RegionView.as_view(), name="region"),
    path("", UniverseView.as_view(), name="universe"),
]
