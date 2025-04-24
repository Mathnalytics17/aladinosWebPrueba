from django.db import models

class Formulario(models.Model):
    no_iban = models.CharField(max_length=100, default="ES2222222222222222", blank=True, null=True)
    
    GENERO_CHOICES = [
        ('masculino', 'masculino'),
        ('femenino', 'femenino')
    ]
    nombre_asterisco = models.CharField(max_length=1222, default='nombre*', blank=True, null=True)
    genero = models.CharField(max_length=12, choices=GENERO_CHOICES, default='masculino', blank=True, null=True)
    created_at = models.DateField(default='2011-03-11', blank=True, null=True)
    fundraiser_name = models.CharField(default='2222', max_length=225, blank=True, null=True)
    fundraiser_code = models.CharField(default='2222', max_length=225, blank=True, null=True)
    
    SALUDO_CHOICES = [
        ('D.', 'Don'),
        ('Dña.', 'Doña')
    ]
    saludo = models.CharField(max_length=4, choices=SALUDO_CHOICES, default='D.', blank=True, null=True)
    primer_canal_captacion = models.CharField(max_length=100, default='F2F Boost Impact (Madrid)', blank=True, null=True)
    canal_entrada = models.CharField(max_length=10, default='F2F', blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    
    TIPO_IDENTIFICACION_CHOICES = [
        ('NIF', 'NIF'),
        ('NIE', 'NIE'),
        ('Pasaporte', 'Pasaporte'),
        ('CIF', 'CIF')
    ]
    tipo_identificacion = models.CharField(max_length=20, choices=TIPO_IDENTIFICACION_CHOICES, default='NIF', blank=True, null=True)
    numero_identificacion = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    via_principal = models.CharField(max_length=255, blank=True, null=True)
    cp_direccion = models.CharField(max_length=5, blank=True, null=True)
    ciudad_direccion = models.CharField(max_length=100, blank=True, null=True)
    estado_provincia = models.CharField(max_length=100, blank=True, null=True)
    
    recibe_memoria = models.CharField(max_length=2, default='SI', blank=True, null=True)
    recibe_correspondencia = models.CharField(max_length=20, default='SI', blank=True, null=True)
    
    movil = models.CharField(max_length=1000, blank=True, null=True)
    telefono_casa = models.CharField(max_length=100, blank=True, null=True)
    correo_electronico = models.EmailField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    importe = models.CharField(max_length=40, default='2222222', blank=True, null=True)
    otra_cantidad = models.CharField(max_length=40, default='2222222', blank=True, null=True)
    
    PERIODICIDAD_CHOICES = [
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual')
    ]
    periodicidad = models.CharField(max_length=20, choices=PERIODICIDAD_CHOICES, default='Mensual', blank=True, null=True)
    
    dia_presentacion = models.CharField(max_length=222, default='0', blank=True, null=True)
    
    medio_pago = models.CharField(max_length=20, default='DOMICILIACIÓN', blank=True, null=True)
    tipo_pago = models.CharField(max_length=20, default='CUOTA', blank=True, null=True)
    
    concepto_recibo = models.CharField(max_length=100, default='GRACIAS POR TU AYUDA - Fundación Aladina', blank=True, null=True)
    
    mandato = models.TextField(blank=True, null=True)
    nombre_autom = models.CharField(max_length=255, blank=True, null=True)
    persona_id = models.CharField(max_length=100, blank=True, null=True)
    nombre_socio = models.CharField(max_length=255, blank=True, null=True)
    tipo_relacion = models.CharField(max_length=20, default='Socio', blank=True, null=True)
    fecha_alta = models.DateField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True, verbose_name="notas")
    is_borrador = models.BooleanField(default=False, verbose_name="borrador")
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}" if self.nombre and self.apellidos else "Formulario sin nombre"