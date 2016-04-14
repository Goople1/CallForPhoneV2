from django import forms

class ClienteForm(forms.Form):
	ruc_dni = forms.CharField(max_length=11, label='Ruc / Ci:',widget=forms.TextInput(attrs={'class':'fillin  form-control','name':'txtRucDni','id':'txtRucDni','placeholder':'Ruc / Ci','spellcheck':'false','title':'Ruc / Ci','required':'true'})) 
	razon_social_nombre = forms.CharField(max_length=70, label='Razon Social / Nombres y Apellidos:',widget=forms.TextInput(attrs={'class':'fillin validated form-control','name':'txtRazonNombre','id':'txtRazonNombre','placeholder':'Razon Social / Nombres y Apellidos','spellcheck':'false','autofocus':'true','title':'Razon Social / Nombres y Apellidos'}))
	correo = forms.EmailField(max_length= 200, label='Correo:',widget=forms.TextInput(attrs={'class':'fillin validated form-control','name':'txtCorreo','id':'txtCorreo','placeholder':'Correo','spellcheck':'false','title':'Correo'})) 
	#tipo_cliente = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Tsrue)                                                                           
	#Mejorarlo
	tipo_cliente_all = (('Lim', 'Lima'),('Pro', 'Provincia'),)
	tipo_cliente=forms.ChoiceField(widget=forms.Select({'class':'fillin  form-control','name':'cmbTipoCliente','id':'cmbTipoCliente','spellcheck':'false','title':'Tipo Cliente','required':'true'}), choices=tipo_cliente_all)
	direccion = forms.CharField(max_length=70, label='Direccion:',widget=forms.TextInput(attrs={'class':'fillin validated form-control','name':'txtDireccion','id':'txtDireccion','placeholder':'direccion','spellcheck':'false','title':'Direccion'}))
	