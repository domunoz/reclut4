#coding:utf-8
import datetime
from django.contrib import admin
from django.utils.datastructures import MultiValueDictKeyError
from daterange_filter.filter import DateRangeFilter
from models import Postulante, Instalacion, Contratado, Supervisor, Cliente, Comuna, Region, Medio
# Register your models here.
class PostulanteAdmin(admin.ModelAdmin):
    list_display= ( 'fecha', 'nombres', 'apellidos',  'comuna', 'ha_sido_condenado_o_detenido', 'industrial', 'contratado',  'medio1',)#  'observaciones',  ) list_filter =  (  'contratado',  ('fecha', DateRangeFilter),  'medio1', 'comuna')
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
    fields = ('nombre', )
    list_display = ('nombre', 'contratados', 'postulantes', 
'contratados_total', 'postulantes_total',) 
    list_filter = (('postulantes_ingresados__fecha', DateRangeFilter),)


    def postulantes(self, obj):
        total_postulantes = Postulante.objects.filter(medio1=obj,
fecha__gte=self.from_date, fecha__lte=self.to_date).count()
        obj.total_postulantes = total_postulantes
        obj.save()
        return obj.total_postulantes

    def postulantes_total(self, obj):
        return Postulante.objects.filter(fecha__gte=self.from_date, 
fecha__lte=self.to_date).count()

    def contratados(self, obj):
        total_contratado = Postulante.objects.filter(medio1=obj,
fecha__gte=self.from_date, fecha__lte=self.to_date,contratado=True).count()
        obj.total_contratado = total_contratado
        obj.save()
        return obj.total_contratado


    def contratados_total(self, obj):
        return Postulante.objects.filter(contratado=True, fecha__gte=self.from_date, fecha__lte=self.to_date).count()


    def changelist_view(self, request, extra_context=None):
        try:
            self.from_date = request.GET['postulantes_ingresados__fecha__gte']
            self.to_date = request.GET['postulantes_ingresados__fecha__lte']


            try:
                self.from_date = datetime.datetime.strptime(self.from_date, '%d-%m-%y').strftime('%Y-%m-%d')  
            except ValueError:
                self.from_date = datetime.datetime(2014,11,01)
   

            try:
                self.to_date = datetime.datetime.strptime(self.to_date, '%d-%m-%y').strftime('%Y-%m-%d')  
            except ValueError:
                self.to_date= datetime.datetime.now().date()
        
        except MultiValueDictKeyError:
            self.from_date = datetime.datetime(2014,11,01)
            self.to_date = datetime.datetime.now().date()

        return super(MedioAdmin, self).changelist_view(request, extra_context=None) 

    postulantes.admin_order_field = 'total_postulantes'
    contratados.admin_order_field = 'total_contratado'



admin.site.register(Postulante, PostulanteAdmin)
admin.site.register(Instalacion)
#admin.site.register(Contratado)
admin.site.register(Supervisor)
admin.site.register(Cliente)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Medio, MedioAdmin)

admin.site.register(Contratado, ContratadoAdmin)
