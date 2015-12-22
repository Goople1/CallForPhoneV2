# -*- encoding:utf-8 -*-
from django.contrib import admin
from models import TipoProducto, Marca, Producto


class TipoProductoAdmin(admin.ModelAdmin):
	list_display = ('nombre',)
	list_filter  = ('nombre',)
	search_fields = ('nombre',)


class MarcaAdmin(admin.ModelAdmin):
	list_display = ('nombre',)
	list_filter  = ('nombre',)
	search_fields = ('nombre',)

class ProductoAdmin(admin.ModelAdmin):
	list_display = ('codigo','color','precio_x_mayor','precio_x_menor','marca','tipo_producto')
	list_filter = ('codigo','marca','tipo_producto__nombre')
	search_fields = ('codigo','marca','tipo_producto__nombre')
	list_editable = ('marca','tipo_producto','precio_x_mayor','precio_x_menor',)
	


#class MarcaAdmin(admin.ModelAdmin):
#	list_display



# Register your models here.
admin.site.register(TipoProducto,TipoProductoAdmin)
admin.site.register(Marca,MarcaAdmin)
admin.site.register(Producto,ProductoAdmin)




