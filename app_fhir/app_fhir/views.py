from django.shortcuts import render
import requests



def call_external_api(request):
    # URL de l'API REST
    url = "https://fhir.alliance4u.io/api/observation"
    
    # Effectuer la requête GET vers l'API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a échoué
        data = response.json()  # Récupérer les données sous forme de JSON
    except requests.exceptions.HTTPError as err:
        return render(request, 'app_fhir/accueil.html', {'message': f'HTTP error occurred: {err}'})
    except Exception as err:
        return render(request, 'app_fhir/accueil.html', {'message': f'Other error occurred: {err}'})

    # Passer les données reçues à un template
    return render(request, 'app_fhir/accueil.html', {'data': data })




   #PATIENT CREE IMPORTANT  "resourceType": "Patient",  "id": "66df16de99cb8a001240f329",

   

def envoi_observations(request):
    if request.method == 'POST':
        poids = request.POST['poids']
        taille = request.POST['taille']
        date = request.POST['date']
    return render(request,'app_fhir/envoi_observations.html')   
   
   
   #utilisateur 