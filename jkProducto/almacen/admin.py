from django.contrib import admin
from .models import Almacen, DetalleAlmacen

from actions import export_as_csv

# Register your models here.

class DetalleAlmacenAdmin(admin.ModelAdmin):
    list_display = ('producto_id','stock','adicional_stock','fecha_ingreso','get_Mayor','get_Menor',)
#field_options = {'fields': (('stock', 'adicional')),}
    list_filter = ('producto_id',)
    search_fields = ('producto_id__tipo_producto__nombre',)
    list_editable =('adicional_stock',)
    actions = [export_as_csv]
    def get_Mayor(self, obj):
        return obj.producto_id.precio_x_mayor
    def get_Menor(self, obj):
    	return obj.producto_id.precio_x_menor

class AlmacenAdmin(admin.ModelAdmin):
	list_display = ('nombre_empresa','ruc','departamento','fecha_registro', 'descripcion','telefono','celular',)



admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(DetalleAlmacen,DetalleAlmacenAdmin)

