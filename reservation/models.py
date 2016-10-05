from django.db import models
from django.contrib.auth.models import User
from hotels.models import Room

# Create your models here.
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
	
