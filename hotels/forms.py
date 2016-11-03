from django import forms
from .models import Hotel, Room, Service
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.core.exceptions import NON_FIELD_ERRORS

class HotelForm(forms.ModelForm):
	
	class Meta:
		model = Hotel
		fields = ['name', 'city', 'address', 'description', 'email', 'tel', 'image', 'services']
		error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
		
	def __init__(self, *args, **kwargs):
		r = super(HotelForm, self).__init__(*args, **kwargs)
		self.fields['description'].required = False
		self.fields['image'].required = False
		self.fields['services'].required = False
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
