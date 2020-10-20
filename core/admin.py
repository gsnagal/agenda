from django.contrib import admin
from core.models import Evento

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_evento', 'data_criacao') #Os campos que aparece na tabela
    list_filter = ('titulo', 'usuario') #Adciiona filtros

admin.site.register(Evento, EventoAdmin)
