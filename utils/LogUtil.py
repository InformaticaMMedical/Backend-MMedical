from django.utils import timezone
from productos.models.LogModel import Log

class LogUtil:
    def registrar_log(accion=None, entidad=None, detalle=None, modelo=None, operacion=None, descripcion=None):
       
        try:
            accion_final = (accion or operacion or "").upper()
            entidad_final = entidad or modelo or "SinEntidad"
            detalle_final = detalle or descripcion or ""

            Log.objects.create(
                usuario="Anónimo",
                accion=accion_final,
                entidad=entidad_final,
                detalle=detalle_final,
                fecha=timezone.now()
            )
        except Exception as e:
            print(f"[LogUtil] Error al registrar log: {e}")