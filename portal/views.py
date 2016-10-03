from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
@login_required
def portal_welcome(request):
	"""
	If users are authenticated, direct them to the portal welcome page
	(template index.html). Otherwise, take them to the login page.
	"""
	return render(request, 'portal/index.html', {'request': request})
	
@login_required       
def upload(request):
    if request.method == 'POST':
    	b = request.user
    	form = UserForm(request.POST, instance=b)
    	if form.is_valid():
    		form.save()
		return HttpResponse('Dati aggiornati')
    else:
    	form_data = {
    		'username':request.user.username,
    		'first_name':request.user.first_name,
    		'last_name':request.user.last_name,
    		'email':request.user.email,
    	}
    	form = UserForm(data=form_data)
    return render(request, 'portal/upload.html', {'form' : form})	
