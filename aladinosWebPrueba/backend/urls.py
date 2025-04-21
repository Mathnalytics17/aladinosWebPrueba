"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from apps.formulario.api.views.index import validar_dni,validar_iban
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.formulario.urls')),
    path('api/registro/', include('apps.formulario.api.routes.index')),
    path('api/validar_iban/', validar_iban, name='validar_iban'),

    path('api/validar-dni/', validar_dni, name='validar_dni'),
    path('api/users/', include('apps.areaPrivada.api.routes.users.index')),
  
    path('api/llamadas/', include('apps.areaPrivada.api.routes.areaAministrador.index')),
]
