from django.conf.urls  import patterns,url
from sucursales import views 


urlpatterns = patterns('',

	#url(r'^$',views.filtroproductos , name='filtroproductos'),
	#url(r'^logout/$',views. , name=''),

	url(r'^$', views.mantenimientoSucursal, name='mantenimientoSucursal'),
    url(r'^add/$', views.addSucursal, name='add'),
    url(r'^edit/$', views.editSucursal, name='edit'),
    url(r'^list/$', views.listSucursal, name='list'),
    url(r'^add/(?P<id>[\w-]+)/$', views.addSucursalA,name = 'addSucursalA'),
    url(r'^edit/(?P<id>[\w-]+)/$', views.editSucursalE,name='editSucursalE'),
    url(r'^list/(?P<id>[\w-]+)/$', views.listSucursalL,name='listSucursalL'),
    url(r'^dameStock/$', views.dameStock,name='stock'),
    url(r'^StockDetalleSucursalAlamcen/$', views.StockDetalleSucursalAlmacen,name='stockDetSecAl'),
    url(r'^addProductotoSucursal/$', views.addProductotoSucursal,name='addProductotoSucursal'),   
    url(r'^editProductotoSucursal/$', views.editProductotoSucursal,name='editProductotoSucursal'), 
    url(r'^historialVentas/$', views.historialVentas,name='historialVentas'), 
    url(r'^historialVentas/(?P<id>[\w-]+)/$', views.Historial_ventas_Sucursal_Admin,name='histoSucursalVentasAdm'), 
    url(r'^historialSucursal/$', views.historialSucursal,name='historialSucursal'),
    url(r'^detalle/ver/$', views.ver_detalle,name='algo1'), 
    url(r'^ventasRangoFecha/$', views.getVentasbyDateRange,name='ventas_rango_fechas'),


  	)
