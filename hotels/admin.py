from django.contrib import admin
from .models import Hotel, Room

# Register your models here.
class RoomInline(admin.StackedInline):
	model = Room
	extra = 1

class HotelAdmin(admin.ModelAdmin):
	fieldsets = [
		('User', {'fields': ['user']}),
		('Name', {'fields': ['name']}),
		('City', {'fields': ['city']}),
		('Address', {'fields': ['address']}),
		('Tel.', {'fields': ['tel']}),
		('Email.', {'fields': ['email']}),
		('Description', {'fields': ['description'], 'classes': ['collapse']}),
		('Image', {'fields': ['image']}),
	]
	list_display = ['user', 'name', 'city', 'address', 'tel', 'email', 'image']
	inlines = [RoomInline]
	search_fields = ['name', 'city', 'address', 'tel', 'email']
	
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room)
