from django import forms
from .models import Hotel, Room, Service
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class HotelForm(forms.ModelForm):
	
	class Meta:
		model = Hotel
		fields = ['name', 'city', 'address', 'description', 'email', 'tel', 'image', 'services']
	
	def __init__(self, *args, **kwargs):
		r = super(HotelForm, self).__init__(*args, **kwargs)
		self.fields['description'].required = False
		self.fields['image'].required = False
		choices = self.fields['services'].choices
		self.fields['services'].widget = forms.CheckboxSelectMultiple(choices = choices)
		self.fields['tel'].widget = PhoneNumberPrefixWidget()
		return r								

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['number', 'beds', 'description', 'cost', 'image']
		
	def __init__(self, *args, **kwargs):
		super(RoomForm, self).__init__(*args, **kwargs)
		self.fields['description'].required = False
		self.fields['image'].required = False
