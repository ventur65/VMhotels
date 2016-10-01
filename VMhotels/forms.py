from django.contrib.auth.models import User
from django import forms

class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'first_name', 'last_name']
		
	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = False
		self.fields['last_name'].required = False
