import json
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from productos.models import (
    Producto,
    Atributo,
    ValorAtributoProducto,
    ArchivoProducto,
)


class Command(BaseCommand):
    help = "Importa TODOS los productos desde los JSON del frontend (modo limpio)"

    def handle(self, *args, **options):

        # 📁 Carpeta donde están TODOS los JSON
        base_path = os.path.abspath(
            os.path.join(
                settings.BASE_DIR,
                "..",  # salir de Backend-MMedical
                "Web-MMedical",
                "src",
                "assets",
                "data"
            )
        )

        if not os.path.exists(base_path):
            self.stderr.write(f"No existe la carpeta: {base_path}")
            return

        # 🧾 Lista de archivos JSON a importar
        archivos_json = [
            "conectores.json",
            "dea.json",
            "ecg.json",
            "ekg.json",
            "fibrobroncoscopio.json",
            "fonendoscopio.json",
            "itof.json",
            "laringoscopios.json",
            "mangueras.json",
            "monitores.json",
            "oftalmoscopio.json",
            "otoscopio.json",
            "oxigenoterapia.json",
            "oximetro.json",
            "pani.json",
            "pi.json",
            "spo2.json",
            "temperatura.json",
            "toco.json",
            "trampas-agua.json",
            "videolaringoscopio.json",
            "colchones.json",
        ]

        for archivo in archivos_json:
            ruta_json = os.path.join(base_path, archivo)

            if not os.path.exists(ruta_json):
                self.stderr.write(f"❌ No existe el archivo: {archivo}")
                continue

            self.stdout.write(f"\n📦 Importando archivo: {archivo}")

            with open(ruta_json, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                producto_id = item.get("producto_id")

                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    self.stderr.write(
                        f"⚠️ Producto con id {producto_id} no existe, se omite"
                    )
                    continue

                self.stdout.write(f"  → Procesando: {producto.nombre}")

                # 🔥 MODO LIMPIO
                ValorAtributoProducto.objects.filter(producto=producto).delete()
                ArchivoProducto.objects.filter(producto=producto).delete()

                # 🖼️ Imágenes (solo referencia, siguen en Supabase)
                for url in item.get("imagenes", []):
                    ArchivoProducto.objects.create(
                        producto=producto,
                        filename=os.path.basename(url.split("?")[0]),
                        key=url
                    )

                # 🧬 Características dinámicas
                for car in item.get("caracteristicas", []):
                    nombre_attr = car["label"].strip()
                    valor = car["value"]

                    atributo = (
                        Atributo.objects
                        .filter(nombre__iexact=nombre_attr)
                        .first()
                    )

                    if not atributo:
                        atributo = Atributo.objects.create(
                            nombre=nombre_attr,
                            tipo_atributo="texto"
                        )

                    atributo.categorias.add(producto.categoria)

                    ValorAtributoProducto.objects.create(
                        producto=producto,
                        atributo=atributo,
                        valor_texto=str(valor)
                    )

                self.stdout.write(f"  ✔ Producto importado")

        self.stdout.write("\n✅ IMPORTACIÓN COMPLETA DE TODOS LOS PRODUCTOS")
