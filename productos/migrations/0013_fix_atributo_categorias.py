from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0012_add_atributo_model'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS productos_atributo_categorias (
                id SERIAL PRIMARY KEY,
                atributo_id INTEGER NOT NULL REFERENCES productos_atributo(id) DEFERRABLE INITIALLY DEFERRED,
                categoria_id INTEGER NOT NULL REFERENCES productos_categoria(id) DEFERRABLE INITIALLY DEFERRED,
                UNIQUE (atributo_id, categoria_id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS productos_atributo_categorias CASCADE;"
        )
    ]
