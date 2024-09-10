from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Patient

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('patientId',)}),
    )

admin.site.register(Patient, CustomUserAdmin)
