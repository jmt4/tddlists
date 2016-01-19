from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

# Create your views here.

def persona_login(request):
	user = authenticate(assertion=request.POST['assertion'])
	if user:
		django_login(request, user)
	return HttpResponse('OK')

def logout(request):
	django_logout(request)
	return redirect('/')