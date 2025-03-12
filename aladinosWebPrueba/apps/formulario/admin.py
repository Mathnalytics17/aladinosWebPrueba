from django.contrib import admin
from apps.formulario.api.models.index import Formulario

# Register your models here.

@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    pass
