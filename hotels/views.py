from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Room, Hotel
from .forms import HotelForm
from django import forms

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

def create_hotel(request):
	if request.method == 'POST':
		form = HotelForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponse("Hotel creato")
	elif request.method == 'GET':
		form = HotelForm()
		return render(request, 'hotels/inserthotel.html', {'form': form,})

