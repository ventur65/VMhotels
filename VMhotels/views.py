from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def main_page(request):
	return render(request, 'index.html')
	
def logout_view(request):
	"Log users out and re-direct them to the main page."
	logout(request)
	return HttpResponseRedirect('/')
