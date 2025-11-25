from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


class PerfilUsuario(models.Model):

    ROL_CHOICES = [
        ('JEFE', 'Jefe'),
        ('INFORMATICA', 'Informática'),
        ('VENDEDORA', 'Vendedora'),
        ('OPERADOR_LOGISTICO', 'Operador logístico'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='VENDEDORA')

    usa_contrasena_temporal = models.BooleanField(default=True)

    ultima_sesion = models.DateTimeField(null=True, blank=True)
    ultima_modificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_rol_display()}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    valido_hasta = models.DateTimeField()

    def __str__(self):
        return f"Token de {self.user.email}"


class AuditoriaUsuarios(models.Model):
    ultima_modificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Auditoría usuarios - última modificación"


class ActividadUsuario(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="actividades"
    )
    fecha = models.DateField()

    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "fecha")
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.user.email} - {self.fecha} - {'Activo' if self.activo else 'Inactivo'}"


def registrar_modificacion_usuarios():
    auditoria, _ = AuditoriaUsuarios.objects.get_or_create(id=1)
    auditoria.ultima_modificacion = timezone.now()
    auditoria.save()


def registrar_actividad_usuario(user: User):
    hoy = timezone.localdate()
    ActividadUsuario.objects.update_or_create(
        user=user,
        fecha=hoy,
        defaults={"activo": True},
    )

    perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
    perfil.ultima_sesion = timezone.now()
    perfil.save()
