from django.db import models

class Formulario(models.Model):
    no_iban=models.CharField(max_length=100,default="ES2222222222222222")
    GENERO_CHOICES = [
        ('masculino', 'masculino'),
        ('femenino', 'femenino')
    ]
    nombre_asterisco=models.CharField(max_length=1222,default='nombre*')
    genero = models.CharField(max_length=12, choices=GENERO_CHOICES,default='masculino')
    created_at= models.DateField(default='2011-03-11')
    fundraiser_name=models.CharField(default='2222',max_length=225)
    fundraiser_code=models.IntegerField(default='11111')
    
    SALUDO_CHOICES = [
        ('D.', 'Don'),
        ('Dña.', 'Doña')
    ]
    
    saludo = models.CharField(max_length=4, choices=SALUDO_CHOICES,default='D.')
    primer_canal_captacion = models.CharField(max_length=100, default='F2F Boost Impact (Madrid)')
    canal_entrada = models.CharField(max_length=10, default='F2F')
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    
    TIPO_IDENTIFICACION_CHOICES = [
        ('NIF', 'NIF'),
        ('NIE', 'NIE'),
        ('Pasaporte', 'Pasaporte')
    ]
    tipo_identificacion = models.CharField(max_length=20, choices=TIPO_IDENTIFICACION_CHOICES,default='NIF')
    numero_identificacion = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    
    via_principal = models.CharField(max_length=255)
    cp_direccion = models.CharField(max_length=10)
    ciudad_direccion = models.CharField(max_length=100)
    estado_provincia = models.CharField(max_length=100)
    
    recibe_memoria = models.CharField(max_length=2, default='SI')
    recibe_correspondencia = models.CharField(max_length=20, default='SI')
    
    movil = models.CharField(max_length=20)
    telefono_casa = models.CharField(max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField()
    descripcion = models.TextField(blank=True, null=True)
    
    IMPORTE_CHOICES = [
        ('10€', '10€'),
        ('20€', '20€'),
        ('30€', '30€'),
        ('50€', '50€'),
        ('Otra Cantidad', 'Otra Cantidad')
    ]
    importe = models.CharField(max_length=20, choices=IMPORTE_CHOICES,default='Otra Cantidad')
    otra_cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    PERIODICIDAD_CHOICES = [
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual')
    ]
    periodicidad = models.CharField(max_length=20, choices=PERIODICIDAD_CHOICES,default='Mensual')
    fecha_primer_pago = models.DateField(blank=True, null=True)
    dia_presentacion = models.CharField(max_length=222,default='0')
    
    medio_pago = models.CharField(max_length=20, default='DOMICILIACIÓN')
    tipo_pago = models.CharField(max_length=20, default='CUOTA')
   
    concepto_recibo = models.CharField(max_length=100, default='GRACIAS POR TU AYUDA - Fundación Aladina')
    
    mandato = models.TextField(blank=True, null=True)
    nombre_autom = models.CharField(max_length=255, blank=True, null=True)
    persona_id = models.CharField(max_length=100, blank=True, null=True)
    nombre_socio = models.CharField(max_length=255, blank=True, null=True)
    tipo_relacion = models.CharField(max_length=20, default='Socio')
    fecha_alta = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
