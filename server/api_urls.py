from django.urls import path, include

urlpatterns = [
    path("cotizaciones/", include("ventas.urls")),
]