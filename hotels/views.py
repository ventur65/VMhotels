from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Room, Hotel

# Create your views here.
class HotelDetailView(generic.DetailView):
	model = Hotel
	template_name = 'hotels/hotel_detail.html'
	
#class RoomDetailView(generic.DetailView):
	#model = Room
	#template_name = 'hotels/room_detai.html'
def room_detail(request, hotel_id, room_id):
	hotel = get_object_or_404(Hotel, pk=hotel_id)
	room = get_object_or_404(Room, pk=room_id)
	context = {'hotel': hotel, 'room': room}
	return render(request, 'hotels/room_detail.html', context)

	

