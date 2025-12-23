from django.urls import path
from ventas.views.cotizacion_views import (CrearCotizacionAPIView, AgregarItemAPIView, ObtenerCotizacionAPIView,)

urlpatterns = [
    path("crear/", CrearCotizacionAPIView.as_view()),
    path("<int:cotizacion_id>/agregar-item/", AgregarItemAPIView.as_view()),
    path("<int:cotizacion_id>/", ObtenerCotizacionAPIView.as_view()),
]
