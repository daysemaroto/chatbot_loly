from django.urls import path

from . import views

urlpatterns = [
    path('generar-voz/', views.generar_voz, name='generar_voz'),
]