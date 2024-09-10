from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Patient(AbstractUser):
    patientId = models.CharField(max_length=100, unique=True, blank=False, null=False)
    patientNumber = models.CharField(max_length=100, blank=False, null=False)
    class Genre(models.TextChoices):
        F = "Female", _("Femme")
        M = "Male", _("Homme")
    genre = models.CharField(Genre, max_length=10, default=Genre.M, choices=Genre.choices)
    date_naissance = models.DateField("date de naissance", default='2000-01-01')
    def __str__(self):
        
        return self.username 
    
    