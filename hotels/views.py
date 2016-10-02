from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Room, Hotel
from .forms import HotelForm, RoomForm
from django import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
class HotelDetailView(generic.DetailView):
	model = Hotel
	template_name = 'hotels/hotel_detail.html'
	
def room_detail(request, hotel_id, room_id):
	hotel = get_object_or_404(Hotel, pk=hotel_id)
	room = get_object_or_404(Room, pk=room_id)
	context = {'hotel': hotel, 'room': room}
	return render(request, 'hotels/room_detail.html', context)

@login_required()
def create_hotel(request):
	if request.method == 'POST':
		form = HotelForm(request.POST, request.FILES)
		if form.is_valid():
			h = form.save(commit=False)
			h.user = request.user
			h.save() ##FARE CON TRY-CATCH
			return HttpResponseRedirect("/hotels/"+str(h.id))
	else:
		form = HotelForm()
	return render(request, 'hotels/inserthotel.html', {'form': form,})

@login_required()
def create_room(request, hotel_id):
	if request.method == 'POST':
		h = get_object_or_404(Hotel, pk=hotel_id)
		if request.user == h.user:
			form = RoomForm(request.POST, request.FILES)
			if form.is_valid():
				r = form.save(commit = False)
				r.hotel = h
				r.save() ##FARE CON TRY-CATCH
				return HttpResponseRedirect('/'.join(['/hotels', str(h.pk), str(r.pk)]))
		else: #Caso di user non uguale
			HttpResponse("Non sei il proprietario dell'hotel.")
	else: #caso GET
		form = RoomForm()
	return render(request, 'hotels/insertroom.html', {'form': form,})

@login_required()	
def edit_hotel(request, hotel_id):
    if request.method == 'POST':
    
    	h = get_object_or_404(Hotel, pk=hotel_id)
    	
    	form = HotelForm(request.POST, request.FILES, instance = h)
    	
    	if form.is_valid():
    		if request.user == h.user:
			r = form.save(commit = False)
			r.user = request.user
			r.image = request.FILES['image']
			r.save()
			return HttpResponseRedirect("/hotels/"+str(h.id))
	else:
		return HttpResponse('Dati non validi')
    else:
    
    	h = get_object_or_404(Hotel, pk=hotel_id)
    	
    	form_data = {
    		'name':h.name,
    		'city':h.city,
    		'address':h.address,
    		'description':h.description,
    		'email':h.email,
    		'tel':h.tel,
    		'image':h.image,
    	}
    	form = HotelForm(data=form_data)
    	return render(request, 'hotels/edithotel.html', {'form' : form}) 
    	
@login_required()	
def edit_room(request, hotel_id, room_id):
    if request.method == 'POST':
    
    	h = get_object_or_404(Hotel, pk=hotel_id)
    	r = get_object_or_404(Room, pk=room_id)
    	
    	form = RoomForm(request.POST, request.FILES, instance = r)
    	
    	if form.is_valid():
    		if request.user == h.user:
    			if h.pk == r.hotel.id:
				ro = form.save(commit = False)
				ro.hotel = h
				ro.image = request.FILES['image']
				ro.save()
				return HttpResponseRedirect("/hotels/"+str(h.id)+"/"+str(r.id))
			else:
				return HttpResponse ('Room non appartenente all hotel')
	else:
		return HttpResponse('Dati non validi')
    else:
    
    	r = get_object_or_404(Room, pk=room_id)
    	
    	form_data = {
    		'number':r.number,
    		'beds':r.beds,
    		'description':r.description,
    		'cost':r.cost,
    		'image':r.image,
    	}
    	form = RoomForm(data=form_data)
    	return render(request, 'hotels/editroom.html', {'form' : form})
			
			
			
	
	
	
	
