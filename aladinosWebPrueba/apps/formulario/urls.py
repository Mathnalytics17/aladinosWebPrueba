from django.urls import path
from . import views

urlpatterns = [
  path('', views.photo_wall, name='photo-wall'),
]