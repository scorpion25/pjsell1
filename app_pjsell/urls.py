from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel, name='painel'),
    path('new-send/', views.new_send, name='new_send'),
    path('historico/', views.historico, name='historico'),
    path('definicoes/', views.definicoes, name='definicoes'),
    path('resumo/', views.resumo_config, name='resumo_config'),
    path('enviar/', views.enviar, name='enviar'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('cancelar/<int:relatorio_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('supervisor/', views.painel_superusuario, name='painel_superusuario'),
    path('', views.home, name='home'),

]
