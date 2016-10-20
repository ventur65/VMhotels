from django.db import models
from django.contrib.auth.models import User
from hotels.models import Hotel
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Review(models.Model):
	user = models.ForeignKey(User)
	hotel = models.ForeignKey(Hotel)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	rate = models.PositiveIntegerField(validators = [
												MinValueValidator(1),
												MaxValueValidator(5),
												])
	comment = models.TextField()
	email = models.EmailField()
	created = models.DateTimeField(auto_now_add = True)
	
