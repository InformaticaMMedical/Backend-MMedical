from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0011_producto_modelos_compatibles_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atributo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo_atributo', models.CharField(
                    max_length=10,
                    choices=[
                        ('texto', 'Texto'),
                        ('numero', 'Número'),
                        ('fecha', 'Fecha'),
                        ('booleano', 'Booleano'),
                    ]
                )),
            ],
        ),
        migrations.AddField(
            model_name='atributo',
            name='categorias',
            field=models.ManyToManyField(blank=True, to='productos.categoria'),
        ),
    ]
