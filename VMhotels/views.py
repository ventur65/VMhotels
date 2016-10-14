from django.shortcuts import render
from hotels.models import Hotel, Room
from review.models import Review
from datetime import datetime
from django.db.models import Avg, Min, Max

def main_page(request):
	if request.method == 'GET':
		return render(request, 'index.html')
	return HttpResponseRedirect(reverse('search_results'))
	
def search_results(request):
	dest = request.POST['dest']
	beds = request.POST['beds']
	check_in = datetime.strptime(request.POST['checkin'], "%Y/%m/%d")
	check_out = datetime.strptime(request.POST['checkout'], "%Y/%m/%d")
	days = check_out - check_in
	rl = dict()
	found_entries = Hotel.objects.filter(city=dest, room__beds=beds).distinct()
	if 'rate' in request.POST:
		found_entries = found_entries.annotate(average=Avg('review__rate')).order_by('-average')
	else:
		#found_entries = found_entries.annotate(average=Avg('room__cost')).order_by('average')
		found_entries = found_entries.order_by('room__cost')
	for h in found_entries:
		rl[h] = h.room_set.filter(beds=beds).aggregate(costmin=Min('cost')*days.days, costmax=Max('cost')*days.days)
#		rl[h]['costmin'] *= days.days
#		rl[h]['costmax'] *= days.days
	return render(request, 'search.html', {'found_entries': found_entries, 'days': days.days, 'rl': rl})
