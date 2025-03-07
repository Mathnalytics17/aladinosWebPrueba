# Vista API
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from smtplib import SMTPException
from rest_framework import status
from django.core.mail import send_mail
#Models
from apps.formulario.api.models.index import Formulario
#Serializers
from apps.formulario.api.serializers.index import FormularioSerializer

#GOOGLE SHEETS

from apps.formulario.api.services.services import agregar_a_google_sheets
    # views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
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
            subject_admin = "Nuevo registro"
            message_admin = (
                f"El usuario {registro.nombre} {registro.apellidos} con DNI {registro.numero_identificacion} "
                f"ha enviado su información."
            )
            
            try:
                send_mail(
                    subject_admin,
                    message_admin,
                    'luisjose0317@gmail.com',  # Remitente
                    ['luisjose0317@gmail.com'],  # Destinatario (administrador)
                    fail_silently=False,
                )
            except SMTPException as e:
                print(f"Error al enviar correo al administrador: {e}")

           # Enviar correo de bienvenida al usuario
            subject_user = "Bienvenido a nuestra comunidad"
            message_user = (
                f"Hola {registro.nombre},\n\n"
                "¡Bienvenido! Ahora eres nuestro nuevo socio. Gracias por tu donación.\n\n"
                "Saludos,\nEl equipo de Eventruck"
            )

            try:
                send_mail(
                    subject_user,
                    message_user,
                    'no-reply@eventruck.com',  # Remitente no-reply
                    [registro.correo_electronico],  # Destinatario (usuario)
                    fail_silently=False,
                )
            except SMTPException as e:
                print(f"Error al enviar correo al usuario: {e}")


            agregar_a_google_sheets(serializer.data)  # Agregar a Google Sheets
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


@csrf_exempt  # Desactiva la protección CSRF para esta vista (solo para desarrollo)
def validar_dni(request):
    if request.method == 'POST':
        try:
            # Parsear el cuerpo de la solicitud como JSON
            data = json.loads(request.body.decode('utf-8'))  # Decodificar el cuerpo de la solicitud
            numero_identificacion = data.get('numeroIdentificacion')

            if not numero_identificacion:
                return JsonResponse({'error': 'Número de identificación no proporcionado'}, status=400)

            # Hacer la solicitud a validardni.es
            response = requests.post(
                'https://www.validardni.es/ajax/test/',
                json={'numeroIdentificacion': numero_identificacion},
                headers={'Content-Type': 'application/json'}
            )

            # Devolver la respuesta de validardni.es
            return JsonResponse(response.json(), status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Cuerpo de la solicitud no es un JSON válido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)