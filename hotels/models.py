from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def path_to_hotel_image(instance, filename):
	return '/'.join([instance.name, filename])
	
def path_to_room_image(instance, filename):
	return '/'.join([instance.hotel.name, str(instance.number), filename])


class Hotel(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 50, unique = True)
	city = models.CharField(max_length = 50, default = '')
	address = models.CharField(max_length = 200)
	description = models.CharField(max_length = 1000, blank = True, null = True)
	email = models.EmailField(unique = True)
	tel = models.PositiveIntegerField(unique = True)
	_height = 50
	_width = 50
	image = models.ImageField(upload_to = path_to_hotel_image, 
								height_field = '_height', 
								width_field = '_width',
								null = True, blank = True)
	class Meta:
		unique_together = ('city', 'address')
		
	def __unicode__(self):
		return self.name
	
class Room(models.Model):
	hotel = models.ForeignKey(Hotel)
	beds = models.PositiveSmallIntegerField(default=1)
	number = models.PositiveSmallIntegerField()
	description = models.CharField(max_length = 300, blank = True, null = True)
	cost = models.FloatField()
	_height = 50
	_width = 50
	image = models.ImageField(upload_to = path_to_room_image,
								height_field = '_height',
								width_field = '_width',
								null = True, blank = True)
	class Meta:
		unique_together = ('hotel', 'number')
	
	def __unicode__(self):
		return self.hotel.name + " Room n. " + str(self.number)
		
class Reservation(models.Model):
	user = models.ForeignKey(User)
	room = models.ForeignKey(Room)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	email = models.EmailField()
	tel = models.PositiveIntegerField()
	idate = models.DateField()
	fdate = models.DateField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
