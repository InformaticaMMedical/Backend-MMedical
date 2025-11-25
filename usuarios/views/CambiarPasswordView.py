from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from usuarios.models import PerfilUsuario
from utils.email_utils import enviar_correo_confirmacion_cambio


class CambiarPasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user: User = request.user
        perfil: PerfilUsuario = user.perfil

        password_actual = request.data.get("password_actual")
        password_nueva = request.data.get("password_nueva")

        # Validar si no es contraseña temporal
        if not perfil.usa_contrasena_temporal:
            if not user.check_password(password_actual):
                return Response(
                    {"error": "La contraseña actual es incorrecta."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validación
        if len(password_nueva) < 8:
            return Response(
                {"error": "La contraseña debe tener al menos 8 caracteres."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Guardar la nueva contraseña
        user.set_password(password_nueva)
        user.save()

        # Marcar que ya NO usa contraseña temporal
        perfil.usa_contrasena_temporal = False
        perfil.save()

        # Enviar correo de confirmación
        enviar_correo_confirmacion_cambio(
            email_destino=user.email,
            nombre_usuario=user.first_name
        )

        return Response(
            {"success": "Contraseña cambiada exitosamente."},
            status=status.HTTP_200_OK
        )
