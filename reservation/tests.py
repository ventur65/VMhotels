from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from hotels.models import Room, Hotel
from django.test import TestCase

from .models import Reservation

def create_reserv (iidate, ffdate):
	"""
	 Creates a reservation that controls the start date and the end date
 	"""
 	user_id = User.objects.create_user('prova', 'prova@prova.com')
 	hotel_id = Hotel.objects.create (user=user_id)
 	room_id = Room.objects.create (hotel=hotel_id, number=1, cost=1)
	return Reservation.objects.create (user=user_id, idate=iidate, fdate=ffdate, room=room_id, is_active=True)

class TestBasic(TestCase):
    "Basic tests"
    
    def test_res_with_fdate_in_past(self):
    	idate = datetime.today()
    	fdate = idate - timedelta(days=7)
    	create_reserv (idate, fdate)
    	self.assertTrue(idate < fdate)
    	

    def test_basic(self):
        a = 1
        self.assertEqual(1, a)

    def test_basic_2(self):
        a = 1
        assert a == 1
        	
