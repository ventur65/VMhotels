from django.db import models
from django.contrib.auth.models import User
from hotels.models import Hotel

# Create your models here.
class Review(models.Model):
	user = models.ForeignKey(User)
	hotel = models.ForeignKey(Hotel)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	rate = models.PositiveIntegerField()
	comment = models.CharField(max_length=1000)
	email = models.EmailField()
	created = models.DateTimeField(auto_now_add = True)
	
