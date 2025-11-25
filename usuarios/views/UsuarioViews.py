from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from usuarios.models import (PerfilUsuario, PasswordResetToken, AuditoriaUsuarios, registrar_modificacion_usuarios, ActividadUsuario, registrar_actividad_usuario,)
from usuarios.serializers import (UsuarioSerializer, UsuarioCreateSerializer, UsuarioUpdateSerializer, PerfilActualSerializer,)
from utils.email_utils import (generar_contrasena_temporal, enviar_correo_bienvenida, enviar_correo_confirmacion_cambio, enviar_correo_recuperacion, generar_token_recuperacion, fecha_expiracion_token,)
from django.utils import timezone
from datetime import timedelta, date


class EsJefeOInformatica(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            perfil = request.user.perfil
            return perfil.rol in ['JEFE', 'INFORMATICA']
        except PerfilUsuario.DoesNotExist:
            return False


class UsuarioListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('first_name')
    permission_classes = [permissions.IsAuthenticated, EsJefeOInformatica]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UsuarioCreateSerializer
        return UsuarioSerializer

    def create(self, request, *args, **kwargs):
        serializer = UsuarioCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nombre = serializer.validated_data["nombre"]
        correo = serializer.validated_data["correo"]
        rol = serializer.validated_data["rol"]

        contrasena_temporal = generar_contrasena_temporal()

        user = User.objects.create(
            username=correo,
            email=correo,
            first_name=nombre,
        )
        user.set_password(contrasena_temporal)
        user.save()

        PerfilUsuario.objects.create(
            user=user,
            rol=rol,
            ultima_sesion=None,
            ultima_modificacion=None,
        )

        enviar_correo_bienvenida(correo, nombre, contrasena_temporal)

        registrar_modificacion_usuarios()

        return Response(UsuarioSerializer(user).data, status=status.HTTP_201_CREATED)


class UsuarioRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, EsJefeOInformatica]

    def get_object(self, pk):
        return generics.get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        return Response(UsuarioSerializer(user).data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UsuarioUpdateSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        perfil = user.perfil
        perfil.ultima_modificacion = timezone.now()
        perfil.save()

        registrar_modificacion_usuarios()

        return Response(UsuarioSerializer(user).data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()

        registrar_modificacion_usuarios()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PerfilActualAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        perfil = getattr(user, "perfil", None)

        data = PerfilActualSerializer({
            "id": user.id,
            "nombre": user.first_name or user.username,
            "correo": user.email,
            "rol": perfil.rol if perfil else "",
            "rol_display": perfil.get_rol_display() if perfil else "",
            "usa_contrasena_temporal": perfil.usa_contrasena_temporal if perfil else False,
            "ultima_sesion": perfil.ultima_sesion if perfil else None,
            "ultima_modificacion": perfil.ultima_modificacion if perfil else None,
        }).data

        return Response(data)


class SolicitarRecuperacionPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        correo = request.data.get("correo")

        try:
            user = User.objects.get(email=correo)
        except User.DoesNotExist:
            return Response({"error": "Correo no registrado"}, status=400)

        PasswordResetToken.objects.filter(user=user).delete()

        token = generar_token_recuperacion()
        expiracion = fecha_expiracion_token()

        PasswordResetToken.objects.create(
            user=user,
            token=token,
            valido_hasta=expiracion
        )

        url = f"http://localhost:5173/restablecer-password/{token}"

        enviar_correo_recuperacion(
            email_destino=correo,
            nombre_usuario=user.first_name,
            url=url
        )

        return Response({"message": "Correo enviado"}, status=200)


class RestablecerPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("token")
        nueva = request.data.get("password_nueva")

        try:
            obj = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({"error": "Token inválido"}, status=400)

        if obj.valido_hasta < timezone.now():
            obj.delete()
            return Response({"error": "Token expirado"}, status=400)

        user = obj.user
        user.set_password(nueva)
        user.save()

        obj.delete()

        return Response({"success": "Contraseña restablecida"}, status=200)


class EditarPerfilAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        nombre = request.data.get("nombre")

        if not nombre:
            return Response({"error": "Debe enviar un nombre"}, status=400)

        user.first_name = nombre
        user.save()

        perfil = user.perfil
        perfil.ultima_modificacion = timezone.now()
        perfil.save()

        registrar_modificacion_usuarios()

        return Response({
            "id": user.id,
            "nombre": user.first_name,
            "correo": user.email,
            "rol": perfil.rol,
            "rol_display": perfil.get_rol_display(),
            "ultima_sesion": perfil.ultima_sesion,
            "ultima_modificacion": perfil.ultima_modificacion,
        })


class UltimaModificacionUsuariosAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        auditoria, _ = AuditoriaUsuarios.objects.get_or_create(id=1)

        return Response({
            "ultima_modificacion": auditoria.ultima_modificacion
        })


class RegistrarActividadHoyAPIView(APIView):
    """
    Endpoint sencillo para marcar que el usuario se conectó hoy.
    Lo puedes llamar desde el frontend justo después del login.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        registrar_actividad_usuario(request.user)
        return Response({"ok": True})


class ActividadSemanalUsuariosAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, EsJefeOInformatica]

    def get(self, request):
        hoy = timezone.localdate()
        lunes = hoy - timedelta(days=hoy.weekday())
        viernes = lunes + timedelta(days=4)

        dias = [lunes + timedelta(days=i) for i in range(5)]
        letras = ["L", "M", "X", "J", "V"]

        actividades = ActividadUsuario.objects.filter(
            fecha__range=(lunes, viernes)
        )

        actividades_por_usuario = {}
        for act in actividades:
            actividades_por_usuario.setdefault(act.user_id, set()).add(act.fecha)

        usuarios_data = []
        usuarios_inactivos = 0

        usuarios = User.objects.all().order_by("first_name")

        for user in usuarios:
            perfil = getattr(user, "perfil", None)
            actividad_semana = {}
            activo_alguna_vez = False

            fechas_usuario = actividades_por_usuario.get(user.id, set())

            for letra, dia in zip(letras, dias):
                activo_dia = dia in fechas_usuario
                actividad_semana[letra] = activo_dia
                if activo_dia:
                    activo_alguna_vez = True

            estado_semana = "activo" if activo_alguna_vez else "inactivo"
            if not activo_alguna_vez:
                usuarios_inactivos += 1

            usuarios_data.append({
                "id": user.id,
                "nombre": user.first_name or user.username,
                "correo": user.email,
                "rol": perfil.rol if perfil else "",
                "rol_display": perfil.get_rol_display() if perfil else "",
                "estado_semana": estado_semana,
                "actividad_semana": actividad_semana,
            })

        return Response({
            "usuarios": usuarios_data,
            "usuarios_inactivos": usuarios_inactivos,
            "lunes": lunes,
            "viernes": viernes,
        })


class ActividadDetalleUsuarioAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, EsJefeOInformatica]

    def get(self, request, pk):
        user = generics.get_object_or_404(User, pk=pk)

        tipo = request.query_params.get("tipo", "anio")
        hoy = timezone.localdate()

        try:
            if tipo == "mes":
                anio = int(request.query_params.get("anio", hoy.year))
                mes = int(request.query_params.get("mes", hoy.month))
                fecha_inicio = date(anio, mes, 1)
                if mes == 12:
                    fecha_fin = date(anio, 12, 31)
                else:
                    fecha_fin = date(anio, mes + 1, 1) - timedelta(days=1)

            elif tipo == "rango":
                desde = request.query_params.get("desde")
                hasta = request.query_params.get("hasta")
                if not desde or not hasta:
                    return Response(
                        {"error": "Debe enviar 'desde' y 'hasta' en tipo=rango"},
                        status=400
                    )
                fecha_inicio = date.fromisoformat(desde)
                fecha_fin = date.fromisoformat(hasta)

            else:
                anio = int(request.query_params.get("anio", hoy.year))
                fecha_inicio = date(anio, 1, 1)
                fecha_fin = date(anio, 12, 31)
        except ValueError:
            return Response({"error": "Fechas inválidas"}, status=400)

        if fecha_fin < fecha_inicio:
            return Response({"error": "El rango de fechas es inválido"}, status=400)

        actividades = ActividadUsuario.objects.filter(
            user=user,
            fecha__range=(fecha_inicio, fecha_fin)
        ).order_by("fecha")

        fechas_activas = {a.fecha for a in actividades}

        total_dias = (fecha_fin - fecha_inicio).days + 1
        dias_activo = len(fechas_activas)
        dias_inactivo = total_dias - dias_activo

        detalles = []
        cursor = fecha_inicio
        while cursor <= fecha_fin:
            detalles.append({
                "fecha": cursor.isoformat(),
                "activo": cursor in fechas_activas,
            })
            cursor += timedelta(days=1)

        return Response({
            "usuario": {
                "id": user.id,
                "nombre": user.first_name or user.username,
                "correo": user.email,
            },
            "resumen": {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "total_dias": total_dias,
                "dias_activo": dias_activo,
                "dias_inactivo": dias_inactivo,
            },
            "detalles": detalles,
        })
