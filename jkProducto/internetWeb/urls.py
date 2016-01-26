from django.conf.urls  import patterns,url
from internetWeb import views 


urlpatterns = patterns('',

	url(r'^$',views.filtroproductos , name='filtroproductos'),
	# url(r'^empresa/$',views.empresa , name='empresa'),
	# url(r'^servicio/$',views.servicio , name='servicio'),
	# url(r'^contacto/$',views.contacto , name='contacto'),
	#url(r'^logout/$',views. , name=''),

	#------------------------------------------------------------




  	)