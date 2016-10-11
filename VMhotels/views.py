from django.shortcuts import render
from hotels.models import Hotel, Room
from datetime import datetime

def main_page(request):
	if request.method == 'GET':
		return render(request, 'index.html')
	return HttpResponseRedirect(reverse('search_results'))
	
def search_results(request):
	query_string = request.POST['dest']
	h = Hotel.objects.filter(city=query_string)
	beds = request.POST['beds']
	check_in = datetime.strptime(request.POST['checkin'], "%Y/%m/%d")
	check_out = datetime.strptime(request.POST['checkout'], "%Y/%m/%d")
	found_entries = Room.objects.filter(hotel__in = h, beds=beds).order_by('cost')
	days = check_out - check_in
	return render(request, 'search.html', {'found_entries': found_entries, 'days': days.days})
