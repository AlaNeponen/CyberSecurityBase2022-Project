from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Note
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def index(request):
    return render(request=request, template_name='notes/notes.html')

def register_request(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'User created.')
            return redirect("/notes")
        messages.error(request, form.errors)

    form = CustomUserCreationForm()
    return render (request=request, template_name='notes/register.html', context={'register_form':form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/notes")
			else:
				messages.error(request,"User not found")
		else:
			messages.error(request, form.errors)
	form = AuthenticationForm()
	return render(request=request, template_name="notes/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('/notes')