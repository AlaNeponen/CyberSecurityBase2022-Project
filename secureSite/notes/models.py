from django.db import models

from django.contrib.auth.models import User

class Note(models.Model):
    content = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)