from django.utils import timezone
from productos.models.LogModel import Log

class LogUtil:
    @staticmethod
    def registrar_log(usuario=None, accion=None, entidad=None, detalle=None, operacion=None, descripcion=None):
        try:
            accion_final = (accion or operacion or "").upper()
            entidad_final = entidad or "SinEntidad"
            detalle_final = detalle or descripcion or ""

            # Guardar ID si usuario es objeto User, sino None
            usuario_id = getattr(usuario, "id", usuario) if usuario else None

            Log.objects.create(
                usuario=usuario_id,
                accion=accion_final,
                entidad=entidad_final,
                detalle=detalle_final,
                fecha=timezone.now()
            )
        except Exception as e:
            print(f"[LogUtil] Error al registrar log: {e}")
