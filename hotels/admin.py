from django.contrib import admin
from .models import Hotel, Room, Service

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
		('Services', {'fields': ['services']}),
	]
	list_display = ['user', 'get_services', 'name', 'city', 'address', 'tel', 'email', 'image']
	inlines = [RoomInline]
	search_fields = ['name', 'city', 'address', 'tel', 'email']

class ServiceAdmin(admin.ModelAdmin):
	list_display = ['name']
	
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room)
admin.site.register(Service, ServiceAdmin)
