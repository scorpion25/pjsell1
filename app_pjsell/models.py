from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Contato(models.Model):
    numero = models.CharField(max_length=20)
    pon = models.CharField(max_length=50)
    data_m1 = models.DateTimeField(auto_now_add=True)
    data_m2 = models.DateTimeField(null=True, blank=True)
    data_m3 = models.DateTimeField(null=True, blank=True)
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.numero} - {self.pon}'


class Configuracao(models.Model):
    mensagem_1 = models.TextField(blank=True)
    mensagem_2 = models.TextField(blank=True)
    data_mensagem_2 = models.DateField(null=True, blank=True)
    hora_mensagem_2 = models.TimeField(null=True, blank=True)
    mensagem_3 = models.TextField(blank=True)
    data_mensagem_3 = models.DateField(null=True, blank=True)
    hora_mensagem_3 = models.TimeField(null=True, blank=True)

    def __str__(self):
        return "Definições do sistema"
    
class RelatorioEnvio(models.Model):
    numero = models.CharField(max_length=20)
    pon = models.CharField(max_length=50)
    data_m1 = models.DateTimeField()
    data_m2 = models.DateTimeField(null=True, blank=True)
    data_m3 = models.DateTimeField(null=True, blank=True)
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    cancelado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero} - {self.funcionario.username}"
