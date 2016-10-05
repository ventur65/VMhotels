from django.contrib import admin
from .models import Reservation

# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
	fieldsets = [
		('User', {'fields': ['user']}),
		('Room', {'fields': ['room']}),
		('IDate', {'fields': ['idate']}),
		('FDate', {'fields': ['fdate']}),
	]
	list_display = ['user', 'room', 'idate', 'fdate']
	search_fields = ['user', 'room', 'idate', 'fdate']
	
admin.site.register(Reservation, ReservationAdmin)
