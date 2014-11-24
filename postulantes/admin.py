#coding:utf-8
from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from models import Postulante, Instalacion, Contratado, Supervisor, Cliente, Comuna, Region, Medio
# Register your models here.
class PostulanteAdmin(admin.ModelAdmin):
    list_display= ( 'fecha', 'medio1', 'nombres', 'apellidos',  'comuna', 'ha_sido_condenado_o_detenido', 'industrial', 'contratado', )#  'observaciones',  ) list_filter =  (  'contratado',  ('fecha', DateRangeFilter),  'medio1', 'comuna')
#    list_editable = ('ha_sido_condenado_o_detenido',)
#    list_editable = ('medio', 'medio1',)
    list_filter = ('contratado', ('fecha', DateRangeFilter), 'medio1', 'comuna')
#    radio_fields = {'sexo': admin.VERTICAL, 'escolaridad': admin.HORIZONTAL }

    search_fields = ('nombres', 'apellidos', 'rut',) 
    fieldsets = (
        ('', {'fields': ('fecha', 'medio1', 'nombres','apellidos', 'rut', 'domicilio', 'comuna',
         'ubicacion',  'telefono', 'email', ('ha_sido_condenado_o_detenido', 'motivo'), 'industrial',  'contratado',  'observaciones' ,)}),
       # ('Información personal', {'fields': ()}),
       # ('Información de contacto', {'fields': ()}),
       # ('Otros', {'fields': (  
       #  ) }),
         #('fecha_contratacion', 'instalacion')#
    )


class ContratadoAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'fecha_contratacion', 'instalacion', 'fecha_de_nacimiento', 'os10', 'vencimiento', )
    fieldsets = (
    ('', {'fields':('nombres', 'apellidos', 'fecha_de_nacimiento', ('os10', 'vencimiento'), 'instalacion')}),
     
    )
    list_filter = ('os10', 'fecha_contratacion')


class MedioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_postulantes', 'contratados', )

    def total_postulantes(self, obj):
   #     return obj.nombre
        return Postulante.objects.filter(medio1=obj).count()

    def contratados(self, obj):
        return Postulante.objects.filter(medio1=obj, contratado=True).count()       
      


admin.site.register(Postulante, PostulanteAdmin)
admin.site.register(Instalacion)
#admin.site.register(Contratado)
admin.site.register(Supervisor)
admin.site.register(Cliente)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Medio, MedioAdmin)

admin.site.register(Contratado, ContratadoAdmin)
