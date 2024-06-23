from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.Login),
    path("signup/", views.signup),
    path("logout/", views.Logout),
    path("blockchain/", views.blockchain),
]
