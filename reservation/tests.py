from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from hotels.models import Room, Hotel
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from .models import Reservation
from .views import *
from .forms import ReservationForm
from django.test.client import Client

def create_reserv (ffdate):
	"""
	 Creates a reservation that controls the start date and the end date
 	"""
 	iidate = datetime.today()
 	user_id = User.objects.create_user('prova', 'prova@prova.com')
 	hotel_id = Hotel.objects.create (user=user_id)
 	room_id = Room.objects.create (hotel=hotel_id, number=1, cost=1)
 	Reservation.objects.create (user=user_id, idate=iidate, fdate=ffdate, room=room_id, is_active=True)
	return iidate

class TestBasic(TestCase):
    "Basic tests"
    
    def setUp(self):	
    	self.factory = RequestFactory()
 	self.user = User.objects.create_user(username='prova', email='ciao@mail.it', password = 'prova')
	self.hotel = Hotel.objects.create(user=self.user)
	self.room = Room.objects.create(hotel=self.hotel, number=1, cost=1)
	iidate = datetime.now().date()
	ffdate = datetime.now().date() + timedelta(days=7)
	self.res = Reservation.objects.create(user=self.user, idate=iidate, fdate=ffdate, room=self.room, is_active=True)
	self.c = Client()

    
    def test_res_with_fdate_in_past(self):
    	fdate = self.res.fdate
    	idate = self.res.idate
    	self.assertFalse(idate < fdate)
    	
    def test_res_with_same_idate(self):
    	iidate = self.res.idate
    	ffdate = self.res.fdate
    	uprova = User.objects.create_user(username='Giova', email='gio@mail.it')
    	instance = Reservation.objects.create(user=uprova, idate=iidate, fdate=ffdate, room=self.room, is_active=True, tel='+393335661378')
    	self.assertTrue(check_res(instance,self.room))
    	
    def test_add_reservation(self):
    	self.c.login(username='prova', password='prova')
    	iidate = datetime.now().date() + timedelta(days=10)
	ffdate = datetime.now().date() + timedelta(days=18)   	
	
	request = self.client.post("include url to post the data given ---->CIAO VENTU QUALE CAZZO E'", {'firstname': 'john', 'lastname': 'prov', 'idate': iidate, 'fdate': ffdate, 'city': 'fabbrico', 'address': 'ciao', 'email': 'prova@gmail.com', 'tel': '+393335661379'})
	#response = add_reservation(request, self.hotel, self.room)
	self.assertEqual(request.status_code, 200)

       
           	
        	
