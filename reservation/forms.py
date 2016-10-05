from django import forms
from hotels.models import Hotel, Room
from .models import Reservation
from bootstrap3_datetime.widgets import DateTimePicker

class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['firstname', 'lastname', 'idate', 'fdate', 'city', 'address', 'email', 'tel']
	def __init__(self, *args, **kwargs):
		super(ReservationForm, self).__init__(*args, **kwargs)
		self.fields['idate'].widget = DateTimePicker(options={"format": "YYYY-MM-DD",
								     "pickTime": False})
		self.fields['fdate'].widget = DateTimePicker(options={"format": "YYYY-MM-DD",
								     "pickTime": False})
	
