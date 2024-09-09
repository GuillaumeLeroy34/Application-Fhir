import requests
from django.shortcuts import render



def call_external_api(request):
    # URL de l'API REST
    url = "https://api.example.com/data"
    
    # Effectuer la requête GET vers l'API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie si la requête a échoué
        data = response.json()  # Récupérer les données sous forme de JSON
    except requests.exceptions.HTTPError as err:
        return render(request, 'error.html', {'message': f'HTTP error occurred: {err}'})
    except Exception as err:
        return render(request, 'error.html', {'message': f'Other error occurred: {err}'})

    # Passer les données reçues à un template
    return render(request, 'data.html', {'data': data})