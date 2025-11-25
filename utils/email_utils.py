import random
import string
import secrets
from datetime import timedelta

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def generar_contrasena_temporal(longitud=10):
    caracteres = (
        string.ascii_letters + string.digits + "!@#$%^&*"
    )
    return ''.join(random.choice(caracteres) for _ in range(longitud))


def enviar_correo_bienvenida(email_destino, nombre_usuario, contrasena_temporal):
    asunto = "Bienvenido/a al sistema MMedical"
    mensaje = (
        f"Hola {nombre_usuario},\n\n"
        f"Tu cuenta ha sido creada exitosamente en MMedical.\n\n"
        f"➡ Tu contraseña temporal es: {contrasena_temporal}\n\n"
        f"Por razones de seguridad, cambia tu contraseña al iniciar sesión.\n\n"
        f"Saludos,\n"
        f"Equipo MMedical"
    )

    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_destino],
        fail_silently=False,
    )


def enviar_correo_confirmacion_cambio(email_destino, nombre_usuario):
    asunto = "Tu contraseña ha sido cambiada exitosamente"
    mensaje = (
        f"Hola {nombre_usuario},\n\n"
        f"Queremos informarte que tu contraseña ha sido actualizada.\n"
        f"Si tú realizaste este cambio, no se requiere ninguna acción.\n"
        f"Si no fuiste tú, contacta al administrador inmediatamente.\n\n"
        f"Saludos,\n"
        f"Equipo MMedical"
    )

    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_destino],
        fail_silently=False,
    )


# ------------------------------------------------------------
# Enviar correo de recuperación de contraseña
# ------------------------------------------------------------
def enviar_correo_recuperacion(email_destino, nombre_usuario, url):
    asunto = "Recuperación de contraseña - MMedical"
    mensaje = (
        f"Hola {nombre_usuario},\n\n"
        f"Hemos recibido una solicitud para restablecer tu contraseña.\n\n"
        f"Si tú realizaste esta solicitud, puedes continuar usando el siguiente enlace:\n\n"
        f"{url}\n\n"
        f"Este enlace es válido por 1 hora por razones de seguridad.\n\n"
        f"Si no solicitaste un cambio de contraseña, simplemente ignora este mensaje.\n"
        f"Nadie puede modificar tu contraseña sin este enlace.\n\n"
        f"Saludos,\n"
        f"Equipo MMedical"
    )

    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_destino],
        fail_silently=False,
    )


def generar_token_recuperacion():
    return secrets.token_urlsafe(48)


def fecha_expiracion_token():
    return timezone.now() + timedelta(hours=1)
