from django.contrib import admin
from .models import Almacen, DetalleAlmacen
from productos.models import Producto
from actions import export_as_csv

# Register your models here.

class DetalleAlmacenAdmin(admin.ModelAdmin):
    list_display = ('info','stock','adicional_stock','fecha_ingreso','precio_Mayor','precio_Menor',)
#field_options = {'fields': (('stock', 'adicional')),}
    list_filter = ('producto_id__codigo',)
    search_fields = ['producto_id__tipo_producto__nombre','producto_id__codigo']
    list_editable =('adicional_stock',)
    actions = [export_as_csv]
    def get_form(self, request, obj=None, **kwargs):
        form = super(DetalleAlmacenAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            #agregar           
            detalle_sucursal_almacen_productos = DetalleAlmacen.objects.all()
            id_producto_detalle_sucu_almacen = [deta.producto_id.id for deta in  detalle_sucursal_almacen_productos]
            form.base_fields['producto_id'].queryset = Producto.objects.exclude(pk__in = id_producto_detalle_sucu_almacen)
            return form
        #modificar
        try:
            form.base_fields['producto_id'].queryset = Producto.objects.filter(pk = obj.producto_id.id)
        except Exception, e:
            print e
        return form

    def precio_Mayor(self, obj):
        return obj.producto_id.precio_x_mayor

    def precio_Menor(self, obj):
    	return obj.producto_id.precio_x_menor

    def info(self, obj):
        return " %s  %s  %s  %s" %(obj.producto_id.tipo_producto.nombre ,  obj.producto_id.marca.nombre, obj.producto_id.codigo, obj.producto_id.get_color_display())

    





    # def get_codigo(self,obj):
    #     return obj.producto_id.codigo

class AlmacenAdmin(admin.ModelAdmin):
	list_display = ('nombre_empresa','ruc','departamento','fecha_registro', 'descripcion','telefono','celular',)



admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(DetalleAlmacen,DetalleAlmacenAdmin)

