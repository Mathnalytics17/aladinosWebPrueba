# Vista API
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from smtplib import SMTPException
from rest_framework import status
from django.core.mail import send_mail
from rest_framework import viewsets
#Models
from apps.formulario.api.models.index import Formulario
from apps.areaPrivada.api.models.users.index import Socio
#Serializers
from apps.formulario.api.serializers.index import FormularioSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from .ibanValidator.openibanlib import openiban
from .ibanValidator.openibanlib.exceptions import IBANFormatValidationException
#GOOGLE SHEETS
from django.contrib.auth import get_user_model

from apps.formulario.api.services.services import agregar_a_google_sheets,agregar_a_google_sheetsBotonGuardarBorrador2

from apps.formulario.api.services.servicesGuardarFormulario import agregar_a_google_sheetsBotonGuardarBorrador


# views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .pythonstdnum.stdnum.es import cif,nif,nie,postal_code
User = get_user_model()
def generar_pdf(html_template, context={}):
    html_string = render_to_string(html_template, context)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=result)

    if pdf.err:
        return None
    return result.getvalue()

def enviar_correo_con_pdf(destinatario,registro):
    
    pdf_content = generar_pdf("formpdf.html",  {
        'nombre': registro['nombre'],
        'apellidos': registro['apellidos'],
        'numero_identificacion': registro['numero_identificacion'],
        'fecha_nacimiento': registro['fecha_nacimiento'],
        'genero': registro['genero'],
        'direccion': registro['via_principal'],
        'cp': registro['cp_direccion'],
        'poblacion': registro['ciudad_direccion'],
        'provincia': registro['estado_provincia'],
        'telefono_movil': registro['movil'],
        'telefono_casa': registro['telefono_casa'],
        'correo_electronico': registro['correo_electronico'],
        'iban': registro['no_iban'],
        'firma_captador':registro['firma_captador'],
        'firma_socio':registro['firma_socio'],
        'importe': registro['importe'],
        'periodicidad': registro['periodicidad'],
        
        'dia_presentacion':datetime.now().strftime("%d/%m/%y"),
    })

    if not pdf_content:
        return "Error al generar el PDF"

    email = EmailMessage(
        subject="Reporte en PDF",
        body="Adjunto encontrarás el reporte en PDF.",
        from_email="socios@altasfundacionaladina.org",
        to=[destinatario],
    )
    email.attach("Copia de Socio. Fundación Aladina.pdf", pdf_content, "application/pdf")
    email.send()
    return "Correo enviado correctamente"



def formatear_fecha(fecha):
    """
    Convierte una fecha en formato ISO (YYYY-MM-DD) a formato dd/mm/yyyy.
    """
    if fecha:
        return datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
    return fecha

def transformar_fechas(data):
    """
    Transforma las fechas en el diccionario `data` al formato dd/mm/yyyy.
    """
    columnas_fecha = [
        "fecha_nacimiento",
        
    ]

    for columna in columnas_fecha:
        if columna in data:
            data[columna] = formatear_fecha(data[columna])

    return data


class FormularioCreateView(generics.CreateAPIView):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
       
        dia = data.pop("dia", None)
        mes = data.pop("mes", None)
        anio = data.pop("anio", None)
        if dia and mes and anio:
            data["fecha_nacimiento"] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
	    
            registro = serializer.save()
            # Enviar correo de notificación al administrador
            subject = f"Nuevo Alta de Socio: {registro.nombre} {registro.apellidos}"
            html_message = render_to_string('email_admin.html', {
                'nombre': registro.nombre,
                'apellidos': registro.apellidos,
                'numero_identificacion': registro.numero_identificacion,
                'telefono': registro.movil,
                'direccion': registro.via_principal,
                'cp': registro.cp_direccion,
                'provincia': registro.estado_provincia,
                'poblacion': registro.ciudad_direccion,
                'correo_electronico': registro.correo_electronico,
                'iban': registro.no_iban,
                'cuota': registro.importe,
                'periodicidad': registro.periodicidad,
                'fecha_recibo': datetime.now().strftime("%d/%m/%Y"),
                'fecha_actual': datetime.now().strftime("%d/%m/%Y"),
            })
            # Crear el correo electrónico
            email = EmailMessage(
                subject,
                html_message,
                "Fundación Aladina <socios@altasfundacionaladina.org>",
                ["socios@altasfundacionaladina.org"]
            )
            email.content_subtype = "html"  # Establecer el contenido como HTML

            try:
                # Generar el PDF
                pdf_content = generar_pdf("formpdf.html", {
                    'nombre': data['nombre'],
                    'apellidos': data['apellidos'],
                    'numero_identificacion': data['numero_identificacion'],
                    'fecha_nacimiento': data['fecha_nacimiento'],
                    'genero': data['genero'],
                    'direccion': data['via_principal'],
                    'cp': data['cp_direccion'],
                    'poblacion': data['ciudad_direccion'],
                    'provincia': data['estado_provincia'],
                    'telefono_movil': data['movil'],
                    'telefono_casa': data['telefono_casa'],
                    'correo_electronico': data['correo_electronico'],
                    'iban': data['no_iban'],
                    'firma_captador': data['firma_captador'],
                    'firma_socio': data['firma_socio'],
                    'importe': data['importe'],
                    'periodicidad': data['periodicidad'],
                    'dia_presentacion': datetime.now().strftime("%d/%m/%y"),
                })

                if not pdf_content:
                    print("Error: No se pudo generar el PDF.")
                    return "Error al generar el PDF"

                # Adjuntar el PDF al correo
                email.attach("Copia de Socio. Fundación Aladina.pdf", pdf_content, "application/pdf")

                # Enviar el correo
                email.send()
                print("Correo enviado correctamente.")

            except SMTPException as e:
                print(f"Error al enviar el correo: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

            subject = "¡Hemos recibido tu alta en Fundación Aladina!"
            html_message = render_to_string('email_client.html', {
                'nombre': registro.nombre,
            })

            # Crear el correo electrónico
            email = EmailMessage(
                subject,
                html_message,
                "Fundación Aladina <socios@altasfundacionaladina.org>",
                [registro.correo_electronico]
            )
            email.content_subtype = "html"  # Establecer el contenido como HTML

            try:
                # Generar el PDF
                pdf_content = generar_pdf("formpdf.html", {
                    'nombre': data['nombre'],
                    'apellidos': data['apellidos'],
                    'numero_identificacion': data['numero_identificacion'],
                    'fecha_nacimiento': data['fecha_nacimiento'],
                    'genero': data['genero'],
                    'direccion': data['via_principal'],
                    'cp': data['cp_direccion'],
                    'poblacion': data['ciudad_direccion'],
                    'provincia': data['estado_provincia'],
                    'telefono_movil': data['movil'],
                    'telefono_casa': data['telefono_casa'],
                    'correo_electronico': data['correo_electronico'],
                    'iban': data['no_iban'],
                    'firma_captador': data['firma_captador'],
                    'firma_socio': data['firma_socio'],
                    'importe': data['importe'],
                    'periodicidad': data['periodicidad'],
                    'dia_presentacion': datetime.now().strftime("%d/%m/%y"),
                })

                if not pdf_content:
                    print("Error: No se pudo generar el PDF.")
                    return "Error al generar el PDF"

                # Adjuntar el PDF al correo
                email.attach("Copia de Socio. Fundación Aladina.pdf", pdf_content, "application/pdf")

                # Enviar el correo
                email.send()
                print("Correo enviado correctamente.")

            except SMTPException as e:
                print(f"Error al enviar el correo: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            datos = {
    "apellidos": data["apellidos"],
    "canal_entrada": data["canal_entrada"],
    "ciudad_direccion": data["ciudad_direccion"],
    "concepto_recibo": data["concepto_recibo"],
    "correo_electronico": data["correo_electronico"],
    "cp_direccion": data["cp_direccion"],
    
    "descripcion": data["descripcion"],
    "dia_presentacion": data["dia_presentacion"],
    "estado_provincia": data["estado_provincia"],
    "fecha_alta": data["fecha_alta"],
    "fecha_nacimiento": data["fecha_nacimiento"],
    "fundraiser_code": data["fundraiser_code"],
    "fundraiser_name": data["fundraiser_name"],
    "genero": data["genero"],
    
    "importe": data["importe"],
    "mandato": data["mandato"],
    "medio_pago": data["medio_pago"],
    "movil": data["movil"],
    "no_iban": data["no_iban"],
    "nombre": data["nombre"],
    "nombre_asterisco": data["nombre_asterisco"],
    "nombre_autom": data["nombre_autom"],
   
    "numero_identificacion": data["numero_identificacion"],
    "otra_cantidad": data["otra_cantidad"],
    "periodicidad": data["periodicidad"],
    "persona_id": data["persona_id"],
    "primer_canal_captacion": data["primer_canal_captacion"],
    "recibe_correspondencia": data["recibe_correspondencia"],
    "recibe_memoria": data["recibe_memoria"],
    "saludo": data["saludo"],
    "telefono_casa": data["telefono_casa"],
    "tipo_identificacion": data["tipo_identificacion"],
    "tipo_pago": data["tipo_pago"],
    "tipo_relacion": data["tipo_relacion"],
    "via_principal": data["via_principal"],
    "fecha_ingreso_dato":data["fecha_ingreso_dato"],
    "notas":data["notas"],
    
}
            datos_transformados = transformar_fechas( datos)
            agregar_a_google_sheets(datos_transformados)  # Agregar a Google Sheets
         # Suponiendo que ya existe un usuario con rol COMERCIAL
            fundraiser = User.objects.get(role='COMERCIAL', fundRaiserCode=data["fundraiser_code"])
             # Crear el nuevo socio
            fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           
            socio = Socio.objects.create(
                nombre_socio=data["nombre"],
                apellido_socio=data["apellidos"],
                genero_socio=data["genero"],
                tipo_identificacion_socio=data["tipo_identificacion"],
                numero_identificacion_socio=data["numero_identificacion"],
                fecha_nacimiento=data["fecha_nacimiento"],
                via_principal=data["via_principal"],
                cp_direccion=data["cp_direccion"],
                ciudad_direccion=data["ciudad_direccion"],
                estado_provincia=data["estado_provincia"],
                importe=float(data["importe"]),  # Convertir a float
                periodicidad=data["periodicidad"],
                dia_presentacion=data.get("dia_presentacion"),  # Valor por defecto 5
                medio_pago=data["medio_pago"],
                tipo_pago=data["tipo_pago"],
                fundraiser=fundraiser,
                primer_canal_captacion=data["primer_canal_captacion"],
                canal_entrada=data["canal_entrada"],
                fecha_creacion=fecha_creacion
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FormularioGoogleSheetsView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Transformar las fechas si es necesario (esto es opcional, dependiendo de tu lógica)
        dia = data.pop("dia", None)
        mes = data.pop("mes", None)
        anio = data.pop("anio", None)
        if dia and mes and anio:
            data["fecha_nacimiento"] = f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"

        # Aquí puedes agregar validaciones adicionales si lo necesitas

        # Enviar los datos a Google Sheets
        try:
            agregar_a_google_sheetsBotonGuardarBorrador(data)  # Llama a tu función para enviar datos a Google Sheets
            agregar_a_google_sheetsBotonGuardarBorrador2(data)
            return Response({"message": "Datos enviados a Google Sheets correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al enviar datos a Google Sheets: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt  # Desactiva la protección CSRF para esta vista (solo para desarrollo)
def validar_dni(request):
    if request.method == 'POST':
        try:
            # Leer el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
            numero_identificacion = data.get('numero_identificacion')
            tipoId = data.get('tipoid')

            # Validar que se proporcionó el número de identificación
            if not numero_identificacion:
                return JsonResponse({'valid': False, 'message': 'Número de identificación no proporcionado'}, status=400)

            # Validar el tipo de identificación
            if tipoId not in ['nif', 'nie','pasaporte']:
                return JsonResponse({'valid': False, 'message': 'Tipo de identificación no válido'}, status=400)

            # Validar el DNI o NIE según el tipo
            if tipoId == 'nif':
                    try:
                        nif.validate(numero_identificacion)  # Validar DNI
                        return JsonResponse({'valid': True, 'message': 'DNI válido'}, status=200)
                    except ValueError as e:
                        # Manejar el error específico de formato inválido
                        return JsonResponse({'valid': False, 'message': str(e)}, status=200)

            elif tipoId == 'nie':
                    try:
                        nie.validate(numero_identificacion)  # Validar NIE
                        return JsonResponse({'valid': True, 'message': 'NIE válido'}, status=200)
                    except ValueError as e:
                        # Manejar el error específico de formato inválido
                        return JsonResponse({'valid': False, 'message': str(e)}, status=200)

            else:
                return JsonResponse({'valid': True, 'message': 'NIE válido'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'valid': False, 'message': 'Formato de solicitud inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def validar_iban(request):
    if request.method == 'POST':
        try:
            # Leer el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
            iban = data.get('iban')

            if not iban:
                return JsonResponse({'valid': False, 'message': 'No se proporcionó un IBAN'}, status=400)
            try:
                iban_result=openiban.IBAN.format_validate(iban)
                if iban_result==True:
                    return JsonResponse({'valid': True, 'message': 'IBAN válido'}, status=200)
                else:
                    return JsonResponse({'valid': False, 'message': 'IBAN inválido'}, status=200)
            except IBANFormatValidationException:
                    return JsonResponse({'valid': False, 'message': 'error de algoritmo'}, status=200)
          
        except json.JSONDecodeError:
            return JsonResponse({'valid': False, 'message': 'Formato de solicitud inválido'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    


class FormularioViewSet(viewsets.ModelViewSet):
    queryset = Formulario.objects.all()
    serializer_class = FormularioSerializer
    permission_classes = [AllowAny]  # Permite acceso sin autenticación