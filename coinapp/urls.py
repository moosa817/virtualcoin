from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("setup", views.initial_setup, name="initial_setup"),
    path("make-transaction/", views.make_transaction_view, name="make_transaction"),
    path("blockchain/", views.blockchain_view, name="blockchain"),
]
