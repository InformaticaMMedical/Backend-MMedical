from django.urls import path
from .views import CookieLoginView, LogoutView, RefreshView

urlpatterns = [
    path("login/", CookieLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
]
