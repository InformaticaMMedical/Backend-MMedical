import json
from django.core.management.base import BaseCommand
from productos.models.ProductoModel import Producto
from productos.models.CategoriaModel import Categoria
from pathlib import Path


class Command(BaseCommand):
    help = "Importa productos desde archivos JSON a la base de datos"

    def handle(self, *args, **options):

        BASE_DIR = Path(__file__).resolve().parents[4]

        archivos = [
            ("Web-MMedical/src/assets/data/ampolletas.json", "Ampolletas"),
            ("Web-MMedical/src/assets/data/baterias.json", "Baterías"),
            ("Web-MMedical/src/assets/data/cable-poder.json", "Cable de poder"),
            ("Web-MMedical/src/assets/data/carro-transporte.json", "Carro de transporte"),
            ("Web-MMedical/src/assets/data/celda-oxigeno.json", "Celda de oxigeno"),
            ("Web-MMedical/src/assets/data/colchones.json", "Colchones"),
            ("Web-MMedical/src/assets/data/conectores.json", "Conectores"),
            ("Web-MMedical/src/assets/data/dea.json", "DEA"),
            ("Web-MMedical/src/assets/data/ecg.json", "ECG"),
            ("Web-MMedical/src/assets/data/ekg.json", "EKG"),
            ("Web-MMedical/src/assets/data/fibrobroncoscopio.json", "Fibrobroncoscopio"),
            ("Web-MMedical/src/assets/data/fonendoscopio.json", "fonendoscopio"),
            ("Web-MMedical/src/assets/data/itof.json", "Itof"),
            ("Web-MMedical/src/assets/data/laringoscopios.json", "Laringoscopios"),
            ("Web-MMedical/src/assets/data/mangueras.json", "Mangueras"),
            ("Web-MMedical/src/assets/data/monitores.json", "Monitores"),
            ("Web-MMedical/src/assets/data/oftalmoscopio.json", "Oftalmoscopio"),
            ("Web-MMedical/src/assets/data/otoscopio.json", "Otoscopio"),
            ("Web-MMedical/src/assets/data/oxigenoterapia.json", "Oxigenoterapia"),
            ("Web-MMedical/src/assets/data/oximetro.json", "Oximetro"),
            ("Web-MMedical/src/assets/data/pani.json", "Pani"),
            ("Web-MMedical/src/assets/data/pi.json", "Pi"),
            ("Web-MMedical/src/assets/data/spo2.json", "Spo2"),
            ("Web-MMedical/src/assets/data/temperatura.json", "Temperatura"),
            ("Web-MMedical/src/assets/data/toco.json", "Toco"),
            ("Web-MMedical/src/assets/data/trampas-agua.json", "Trampas de agua"),
            ("Web-MMedical/src/assets/data/videolaringoscopio.json", "Videolaringoscopio"),
        ]

        for ruta_relativa, nombre_categoria in archivos:
            ruta_json = BASE_DIR / ruta_relativa
            self.importar_json(ruta_json, nombre_categoria)

        self.stdout.write(self.style.SUCCESS("✔ Importación finalizada"))

    def importar_json(self, ruta_json, nombre_categoria):

        if not ruta_json.exists():
            self.stdout.write(self.style.WARNING(
                f"⚠ Archivo no encontrado: {ruta_json}"
            ))
            return

        with open(ruta_json, encoding="utf-8") as f:
            data = json.load(f)

        categoria, _ = Categoria.objects.get_or_create(
            nombre=nombre_categoria
        )

        creados = 0
        existentes = 0

        for item in data:
            nombre = item.get("nombre")

            if not nombre:
                continue

            if Producto.objects.filter(nombre=nombre).exists():
                existentes += 1
                continue

            Producto.objects.create(
                nombre=nombre,
                descripcion=item.get("descripcion", ""),
                categoria=categoria
            )
            creados += 1

        self.stdout.write(
            f"📦 {nombre_categoria}: ➕ {creados} | 🔁 {existentes}"
        )
