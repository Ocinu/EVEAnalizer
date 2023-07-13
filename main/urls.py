from django.urls import path

from .views import AboutView, LoginView, LogoutView, NewsView, RegisterView

urlpatterns = [
    path("", NewsView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("about/", AboutView.as_view(), name="about"),
]
