from django.urls import path
from .views import CookieLoginView, LogoutView, RefreshView
from usuarios.views.UsuarioViews import (UsuarioListCreateAPIView, UsuarioRetrieveUpdateDestroyAPIView, PerfilActualAPIView,
    SolicitarRecuperacionPasswordAPIView, RestablecerPasswordAPIView, UltimaModificacionUsuariosAPIView, ActividadSemanalUsuariosAPIView,
    ActividadDetalleUsuarioAPIView,RegistrarActividadHoyAPIView,)
from usuarios.views.CambiarPasswordView import CambiarPasswordAPIView


urlpatterns = [
    path("login/", CookieLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path('perfil/', PerfilActualAPIView.as_view(), name='perfil-actual'),
    path('', UsuarioListCreateAPIView.as_view(), name='usuarios-list-create'),
    path('<int:pk>/', UsuarioRetrieveUpdateDestroyAPIView.as_view(), name='usuarios-detalle'),
    path("cambiar-password/", CambiarPasswordAPIView.as_view()),
    path("password/recuperar/", SolicitarRecuperacionPasswordAPIView.as_view()),
    path("password/restablecer/", RestablecerPasswordAPIView.as_view()),
    path("auditoria/", UltimaModificacionUsuariosAPIView.as_view(), name="auditoria-usuarios"),
    path("actividad/registrar-hoy/", RegistrarActividadHoyAPIView.as_view()),
    path("actividad/semana/", ActividadSemanalUsuariosAPIView.as_view()),
    path("actividad/<int:pk>/", ActividadDetalleUsuarioAPIView.as_view()),
]
