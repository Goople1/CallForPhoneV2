from django import forms

class FormInciarSesion(forms.Form):
	username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'fillin validated form-control','id':'s_input_email','placeholder':'Correo o Usuario','spellcheck':'false','autofocus':'true','title':'Correo o Usuario','required':'true'}))
	password = forms.CharField(widget= forms.PasswordInput(attrs={'class':'fillin validated form-control','id':'s_input_password','placeholder':'Password','title':'Password','required':'true'}))