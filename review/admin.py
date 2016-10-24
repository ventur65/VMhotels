from django.contrib import admin
from .models import Review
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
	fieldsets = [
	('User', {'fields': ['user']}),
	('Hotel', {'fields': ['hotel']}),
	('First Name', {'fields': ['firstname']}),
	('Last Name', {'fields': ['lastname']}),
	('Rate', {'fields': ['rate']}),
	('Comment', {'fields': ['comment'], 'classes': ['collapse']}),
	('Email', {'fields': ['email']}),
	]
	
	list_display = ['user', 'hotel', 'firstname', 'lastname', 'rate']
	search_fields = ['user', 'hotel']
	
admin.site.register(Review, ReviewAdmin)
	
