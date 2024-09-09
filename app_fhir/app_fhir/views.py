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




def post_patient(request):
   data= {
    "resourceType": "Patient",
    "id": "66d875c65dab6800126487f6",
    "name": [
      {
        "use": "official",
        "family": "Receveur",
        "given": [
          "Alexandre"
        ]
      },
      {
        "use": "usual",
        "given": [
          "Alex"
        ]
      }
    ],
    "gender": "female",
    "birthDate": "1974-12-25",
    "deceasedBoolean": false
  }
   
   #PATIENT CREE IMPOETANT
   {
  "resourceType": "Patient",
  "id": "66df16de99cb8a001240f329",
  "name": [
    {
      "use": "official",
      "family": "Ringuet",
      "given": [
        "Dominique"
      ]
    },
    {
      "use": "usual",
      "given": [
        "Golmon"
      ]
    }
  ],
  "gender": "female",
  "birthDate": "1980-01-20",
  "deceasedBoolean": false
}