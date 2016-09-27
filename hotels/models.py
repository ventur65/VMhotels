from django.db import models

# Create your models here.

def path_to_hotel_image(instance, filename):
	return '/'.join([instance.name, filename])
	
def path_to_room_image(instance, filename):
	return '/'.join([instance.hotel.name, str(instance.number), filename])

class Hotel(models.Model):
	name = models.CharField(max_length = 50, unique = True)
	city = models.CharField(max_length = 50, default = '')
	address = models.CharField(max_length = 200, unique = True)
	description = models.CharField(max_length = 1000)
	email = models.EmailField(unique = True)
	tel = models.PositiveIntegerField(unique = True)
	_height = 50
	_width = 50
	image = models.ImageField(upload_to = path_to_hotel_image, 
								height_field = '_height', 
								width_field = '_width',
								null = True)
	
	def __unicode__(self):
		return self.name
	
class Room(models.Model):
	hotel = models.ForeignKey(Hotel)
	beds = models.PositiveSmallIntegerField(default=1)
	number = models.PositiveSmallIntegerField()
	description = models.CharField(max_length = 300)
	cost = models.FloatField()
	_height = 50
	_width = 50
	image = models.ImageField(upload_to = path_to_room_image,
								height_field = '_height',
								width_field = '_width',
								null = True)
	class Meta:
		unique_together = ('hotel', 'number')
	
	def __unicode__(self):
		return self.hotel.name + " Room n. " + str(self.number)
	
	
