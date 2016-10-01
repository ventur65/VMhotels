from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from .forms import RegisterForm

def main_page(request):
	return render(request, 'index.html')

def logout_view(request):
	"Log users out and re-direct them to the main page."
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit = False) ##METTERE TRY
			user.set_password(form.fields['password'])
			user.save()
			g = Group.objects.get(name='owners')
			user.groups.add(g)
			user.user_permissions = [p for p in g.permissions.all()]
			return HttpResponseRedirect('/login')
	else:
		form = RegisterForm()
	return render(request, 'registration.html', {'form': form})	
