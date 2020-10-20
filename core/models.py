from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.

class Evento(models.Model): #models.Model é o parametro
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True) #Pode ser em branco ou nulo também
    data_evento = models.DateTimeField(verbose_name='Data do Evento') #Muda o nome que aparece na tabela
    data_criacao = models.DateTimeField(auto_now=True) #Insere a hora atual quando é feito um registro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #Se o usuario for excluido da aplicação, apaga tudo do usuario


    class Meta: #Faz com que o nome da tabela seja eventos, são os metadados
        db_table = 'evento'

    def __str__(self):
        return  self.titulo #Ao inves de aparecer "object" aparece o titulo, trata o objeto

    def get_data_evento(self): #Transforma o data_evento em outro formato
        return self.data_evento.strftime('%d/%m/%Y %H:%M Hrs')

    def get_data_input_evento(self): #Foramato quando se cria um evento
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self): #Flag
        if self.data_evento < datetime.now():
            return True
        else:
            return False


