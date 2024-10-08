"""
URL configuration for app_fhir project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.call_external_api,name='accueil'),
    path('observations',views.envoi_observations,name='observations'),
    path('connexion',views.login_view,name="connexion"),
    path('inscription', views.register,name= "inscription"),
    path('navigation', views.navigation, name="navigation"),
    path('deconnexion', views.logout_view, name="deconnexion"),
    path('graphique_observation', views.graphique_observation, name = 'graphique_observations'),
    path('bmi-data/', views.get_bmi_data, name='get_bmi_data'), #pas une vraie vue, ça renvoie juste des données en Json
    path('bmi-chart/', views.bmi_chart_view, name='bmi_chart_view'), #la vraie vue qui crée le graphe
    path('compte/',views.compte, name="compte"),
]
