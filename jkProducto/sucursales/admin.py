# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Sucursal, SucursalTrabajador #,Cliente#,EstadoSucursal
#,HistorialSucursal
#from productos.models import Producto, Marca, TipoProducto
#from actions import export_as_csv
# Register your models here.
# class DetalleAlmacenAdmin(admin.ModelAdmin):
#     list_display = ('producto_id','stock','adicional_stock','fecha_ingreso','get_Mayor','get_Menor',)
# #field_options = {'fields': (('stock', 'adicional')),}
#     list_filter = ('producto_id',)
#     search_fields = ('producto_id__tipo_producto__nombre',)
#     list_editable =('adicional_stock',)
#     actions = [export_as_csv]
#     def get_Mayor(self, obj):
#         return obj.producto_id.precio_x_mayor
#     def get_Menor(self, obj):
#     	return obj.producto_id.precio_x_menor

class SucursalAdmin(admin.ModelAdmin):
	list_display = ('codigo_puesto', 'nombre', 'departamento', 'nombre_estado')
	list_filter = ('codigo_puesto', 'departamento','nombre','nombre_estado',)
	search_fields = ('codigo_puesto', 'departamento')
	#list_editable = ('codigo_puesto', 'departamento','id_estadoSucursal',)

class SucursalTrabajadorAdmin(admin.ModelAdmin):
	list_display = ('sucursal','trabajador','fecha_ingreso',)
	list_filter = ('sucursal',)
	search_fields = ('sucursal',)
	#list_editable = ('sucursal',)

#class ClienteAdmin(admin.ModelAdmin):
#	list_display = ('nombre','apellidos','telefono','dni','ruc' ,'correo' , 'direccion')

class AlmacenAdmin(admin.ModelAdmin):
	list_display = ('nombre_empresa','ruc','departamento','fecha_registro', 'descripcion','telefono','celular',)
	#list_editable = ('nombre_empresa','ruc','departamento','descripcion','telefono','celular',)

#list_display = ('codigo','marca','tipo_producto','color','stock','adicional','mayor','menor','fecha_ingreso',)

#admin.site.register(EstadoSucursal)
#admin.site.register(Almacen, AlmacenAdmin)
#admin.site.register(DetalleAlmacen,DetalleAlmacenAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(SucursalTrabajador, SucursalTrabajadorAdmin)
#admin.site.register(Cliente, ClienteAdmin)
