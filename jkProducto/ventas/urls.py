from django.conf.urls  import patterns,url
from ventas import views 

urlpatterns = patterns('',

	url(r'^$',views.home_ventas , name='home_ventas'),
	url(r'^realizarventa/$',views.venta , name='venta'),
	url(r'^addVenta/$',views.addVenta , name='addVenta'),
	
	url(r'^modificar/$',views.modificar_venta, name='modificar'),
	url(r'^modificar/(?P<venta_id>[0-9]+)/$',views.modificar_detalle_ventas, name='detalleventa'),

	#url(r'^reporte/asistencia/$',views.reporte_asistencia, name='reporteAsistencia'),
	url(r'^reporte/stock/$',views.lista_producto , name='reporteStock'),
	url(r'^reporte/venta/$',views.reporte_venta , name='reporteVenta'),
	url(r'^reporte/venta/detalle/$',views.detalle_venta , name='reporteDetalleVenta'),


	url(r'^cargarProductos/$',views.cargar_productos, name='cargar_productos'),
	#url(r'^asistencia/$',views.asistencia , name='asistencia'),
	#url(r'^reporte/$',views.home_empleado_menu_reporte , name='menuReporte'),
	url(r'^home/$',views.home_empleado_menu_reporte , name='home'),





  	)