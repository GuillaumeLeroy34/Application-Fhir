from django.contrib.auth.models import AbstractUser
from django.db import models

class Patient(AbstractUser):
    patientId = models.CharField(max_length=100, unique=True, blank=False, null=False)
    patientNumber = models.CharField(max_length=100, blank=False, null=False)
    def __str__(self):
        return self.username 
    
    