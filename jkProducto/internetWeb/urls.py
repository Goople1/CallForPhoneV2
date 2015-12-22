from django.conf.urls  import patterns,url
from internetWeb import views 

urlpatterns = patterns('',

	url(r'^$',views.filtroproductos , name='filtroproductos'),
	#url(r'^logout/$',views. , name=''),

	#------------------------------------------------------------




  	)