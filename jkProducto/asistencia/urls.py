from django.conf.urls  import patterns,url
from asistencia import views 


app_name = 'asistencia'
urlpatterns = patterns('',

	url(r'^$',views.asistencia , name='asistencia'),
	url(r'^(?i)reporte/$',views.reporte_asistencia, name='reporteAsistencia'),
	url(r'^(?i)historialAsistencia/$',views.historial_asistencia, name='historialAsistencia')

  	)
