from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

def path_to_hotel_image(instance, filename):
	return '/'.join([instance.name, filename])
	
def path_to_room_image(instance, filename):
	return '/'.join([instance.hotel.name, str(instance.number), filename])

class Service(models.Model):
	name = models.CharField(max_length = 30)

	def __unicode__(self):
		return self.name

class Hotel(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length = 50, unique = True)
	city = models.CharField(max_length = 50, default = '')
	address = models.CharField(max_length = 200)
	description = models.TextField(blank = True, null = True)
	email = models.EmailField(unique = True)
	#tel = models.PositiveIntegerField(unique = True)
	#phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    	#tel = models.CharField(validators=[phone_regex], blank=True, max_length = 15, unique = True) # validators should be a list
	tel = PhoneNumberField(unique = True, max_length = 15)
	_height = 50
	_width = 50
	image = models.ImageField(upload_to = path_to_hotel_image, 
								height_field = '_height', 
								width_field = '_width',
								null = True, blank = True)
	services = models.ManyToManyField(Service, blank = True)
	
	class Meta:
		unique_together = ('city', 'address')
		
	def __unicode__(self):
		return self.name
	
	def get_services(self):
		return ', '.join([s.name for s in self.services.all()])
	
class Room(models.Model):
	hotel = models.ForeignKey(Hotel)
	beds = models.PositiveSmallIntegerField(default=1, 
											validators = [
												MinValueValidator(1)
												]
											)
	number = models.PositiveSmallIntegerField(validators = [
												MinValueValidator(1)
												]
											)
	description = models.TextField(blank = True, null = True)
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
