from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.db import connection
from babel.dates import format_datetime
from datetime import datetime

def index(request):
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.all()
    return render(request=request, template_name='notes/notes.html', context={'notes': notes})

@login_required
def add(request):
    content = request.POST.get('note')
    d = datetime.now()
    formatted_date = format_datetime(d, "yyyy.MMMM.dd GGG hh:mm a", locale='en')
    content += f', posted by: {request.user.username}, timestamp: {formatted_date}'
    cursor = connection.cursor()
    id = request.user.id
    query = f"INSERT INTO NOTES (content, owner) VALUES ('{content}', '{id}')"
    cursor.execute(query)

# Fix:
#    query = "INSERT INTO NOTES (content, owner) VALUES (%s, %s)"
#    cursor.execute(query, (content, id))
    return redirect('/notes')

@login_required
def delete(request):
    n = Note.objects.get(pk=request.POST.get('id'))
    n.delete()

# Fix:
#    if n.owner.id == request.user.id:    
#        n.delete()
#    else: 
#        messages.error(request, 'You can only delete your own notes!')
    return redirect('/notes')

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