from django.shortcuts import render
from hotels.models import Hotel

def main_page(request):
	if request.method == 'GET':
		return render(request, 'index.html')
	return HttpResponseRedirect(reverse('search_results'))
	
def search_results(request):
	query_string = request.POST['q']
	found_entries = Hotel.objects.filter(city=query_string)
	return render(request, 'search.html', {'query_string': query_string, 'found_entries': found_entries})
