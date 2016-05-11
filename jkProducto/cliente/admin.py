from django.contrib import admin
from .models import Cliente


class ClienteAdmin(admin.ModelAdmin):
	pass

admin.site.register(Cliente, ClienteAdmin)



# Register your models here.
