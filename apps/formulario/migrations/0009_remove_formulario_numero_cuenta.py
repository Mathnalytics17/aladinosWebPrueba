# Generated by Django 5.1.6 on 2025-03-05 01:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("formulario", "0008_formulario_nombre_asterisco"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="formulario",
            name="numero_cuenta",
        ),
    ]
