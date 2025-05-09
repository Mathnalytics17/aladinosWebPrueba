# Generated by Django 5.1.6 on 2025-04-23 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0003_alter_formulario_numero_identificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulario',
            name='ciudad_direccion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='cp_direccion',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='estado_provincia',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='importe',
            field=models.CharField(blank=True, default='2222222', max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='recibe_correspondencia',
            field=models.CharField(blank=True, default='SI', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='recibe_memoria',
            field=models.CharField(blank=True, default='SI', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='formulario',
            name='via_principal',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
