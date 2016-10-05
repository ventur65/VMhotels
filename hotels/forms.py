from django import forms
from .models import Hotel, Room, Reservation
from django.contrib.admin import widgets

class HotelForm(forms.ModelForm):
	class Meta:
		model = Hotel
		fields = ['name', 'city', 'address', 'description', 'email', 'tel', 'image']
	def __init__(self, *args, **kwargs):
		super(HotelForm, self).__init__(*args, **kwargs)
		self.fields['description'].required = False
		self.fields['image'].required = False

class RoomForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ['number', 'beds', 'description', 'cost', 'image']
		
	def __init__(self, *args, **kwargs):
		super(RoomForm, self).__init__(*args, **kwargs)
		self.fields['description'].required = False
		self.fields['image'].required = False
		
class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['firstname', 'lastname', 'city', 'address', 'email', 'tel', 'idate', 'fdate']
	#def __init__(self, *args, **kwargs):
		#super(ReservationForm, self).__init__(*args, **kwargs)
		#self.fields['idate'].widget = widgets.AdminDateWidget
		#self.fields['fdate'].widget = widgets.AdminDateWidget
	
