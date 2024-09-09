
from django.urls import path, include
import views


app_name = "patient"
urlpatterns = [
    path('accueil/',views.call_external_api)
    
]
