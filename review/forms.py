from django import forms
from hotels.models import Hotel
from .models import Review

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ['firstname', 'lastname', 'rate', 'comment', 'email']
	def __init__(self, *args, **kwargs):
		super(ReviewForm, self).__init__(*args, **kwargs)
		
	
