from django import forms
from .models import Hotel, Room

class HotelForm(forms.ModelForm):
	class Meta:
		model = Hotel
		fields = ['name', 'city', 'address', 'description', 'email', 'tel', 'image']
	def __init__(self, *args, **kwargs):
		super(HotelForm, self).__init__(*args, **kwargs)
		self.fields['description'].required = False
		#Mettere come non obbligatorio anche campo image
		

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['number', 'beds', 'description', 'cost', 'image']
		
	def __init__(self, *args, **kwargs):
		super(RoomForm, self).__init__(*args, **kwargs)
		self.fields['description'].required = False
		#Mettere come non obbligatorio anche campo image
	
