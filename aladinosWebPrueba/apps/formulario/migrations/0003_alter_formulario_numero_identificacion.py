# Generated by Django 5.1.6 on 2025-04-23 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0002_formulario_is_borrador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulario',
            name='numero_identificacion',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
