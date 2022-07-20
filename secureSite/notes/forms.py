import re
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError   
from django.forms.forms import Form 
      
class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
      
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("Username already taken.")  
        return username  

    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']

        #if len(password1) < 8 or bool(re.match('^[0-9]+$', password1)) or password1.isalpha():
        #    raise ValidationError("Password must be atleast 12 characters long and must consist of numbers and letters")
      
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Passwords don't match.")  
        return password2  
      
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user