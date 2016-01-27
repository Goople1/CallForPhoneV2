from django.conf.urls  import patterns,url
from ventas import views 

urlpatterns = patterns('',

	url(r'^$',views.home_ventas , name='home_ventas'),
	url(r'^(?i)realizarventa/$',views.venta , name='venta'),
	url(r'^(?i)addVenta/$',views.addVenta , name='addVenta'),
	
	url(r'^(?i)modificar/$',views.modificar_venta, name='modificar'),
	url(r'^(?i)modificar/(?P<venta_id>[0-9]+)/$',views.modificar_detalle_ventas, name='detalleventa'),

	#url(r'^reporte/asistencia/$',views.reporte_asistencia, name='reporteAsistencia'),
	url(r'^(?i)reporte/stock/$',views.lista_producto , name='reporteStock'),
	url(r'^(?i)reporte/venta/$',views.reporte_venta , name='reporteVenta'),
	url(r'^(?i)reporte/venta/detalle/$',views.detalle_venta , name='reporteDetalleVenta'),


	url(r'^(?i)cargarProductos/$',views.cargar_productos, name='cargar_productos'),
	url(r'^(?i)asistencia/$',views.asistencia , name='asistencia'),
	#url(r'^reporte/$',views.home_empleado_menu_reporte , name='menuReporte'),
	url(r'^(?i)home/$',views.home_empleado_menu_reporte , name='home'),





  	)