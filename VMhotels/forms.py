from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from datetime import date

class SearchForm(forms.Form):
	dest = forms.CharField(max_length=50)
	beds = forms.IntegerField(min_value = 1)
	checkin = forms.DateField()
	checkout = forms.DateField()
	rate = forms.BooleanField(required=False)
	
	def __init__(self, *args, **kwargs):
		super(SearchForm, self).__init__(*args, **kwargs)
		self.fields['checkin'].widget = DateTimePicker(options={"format": "YYYY-MM-DD",
								     "pickTime": False})
		self.fields['checkout'].widget = DateTimePicker(options={"format": "YYYY-MM-DD",
								     "pickTime": False})
								     
	def clean(self):
		cleaned_data = super(SearchForm, self).clean()
		checkin = cleaned_data.get('checkin')
		checkout = cleaned_data.get('checkout')
		
		if checkin and checkout and (checkin >= checkout):
			msg = "Initial Date must be earlier than Final Date"
			self.add_error('checkin', msg)
			self.add_error('checkout', msg)
		
		if checkin and (checkin < date.today()):
			msg = "Date in the past"
			self.add_error('checkin', msg)
		
		if checkout and (checkout < date.today()):
			msg = "Date in the past"
			self.add_error('checkout', msg)
