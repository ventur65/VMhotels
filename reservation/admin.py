from django.contrib import admin
from .models import Reservation

# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
	fieldsets = [
		('User', {'fields': ['user']}),
		('Room', {'fields': ['room']}),
		('First Name', {'fields': ['firstname']}),
		('Last Name', {'fields': ['lastname']}),
		('City', {'fields': ['city']}),
		('Address', {'fields': ['address']}),
		('Email', {'fields': ['email']}),
		('Tel', {'fields': ['tel']}),
		('Initial Date', {'fields': ['idate']}),
		('Final Date', {'fields': ['fdate']}),
		('Is Active', {'fields': ['is_active']}),
	]
	list_display = ['user', 'room', 'idate', 'fdate', 'updated', 'is_active']
	search_fields = ['user', 'room', 'idate', 'fdate', 'is_active']
	
admin.site.register(Reservation, ReservationAdmin)
