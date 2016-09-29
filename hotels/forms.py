from django import forms
from .models import Hotel, Room

class HotelForm(forms.ModelForm):
	class Meta:
		model = Hotel
		fields = ['name', 'city', 'address', 'description', 'email', 'tel', 'image']

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['number', 'beds', 'description', 'cost', 'image']
