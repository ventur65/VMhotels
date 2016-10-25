from django import forms
from hotels.models import Hotel, Room
from .models import Reservation
from bootstrap3_datetime.widgets import DateTimePicker
from datetime import date
from phonenumber_field.widgets import PhoneNumberPrefixWidget

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
		self.fields['tel'].widget = PhoneNumberPrefixWidget()
		
	def clean(self):
		cleaned_data = super(ReservationForm, self).clean()
		idate = cleaned_data.get('idate')
		fdate = cleaned_data.get('fdate')
		
		if idate and fdate and (idate >= fdate):
			msg = "Initial Date must be earlier than Final Date"
			self.add_error('idate', msg)
			self.add_error('fdate', msg)
		
		if idate and (idate < date.today()):
			msg = "Date in the past"
			self.add_error('idate', msg)
		
		if fdate and (fdate < date.today()):
			msg = "Date in the past"
			self.add_error('fdate', msg)
