# Generated by Django 4.2 on 2023-05-01 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0003_empleado_hola_vida'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empleado',
            old_name='hola_vida',
            new_name='hoja_vida',
        ),
    ]
