from django.shortcuts import render, redirect 
import requests
from django.utils import timezone
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


url = 'https://fhir.alliance4u.io/api/'
#adresse de l'api qu'on utilise pour faire transiter les données

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

#ID médecin f011 f010
   
#post une observation: observer la doc, ne pas oublier d'inclure l'identifiant du patient connecté
def envoi_observations(request):
    payloadWeight= {}
    payloadHeight = {}
    headers = {}
    retour_reponse = ""
    date_aware = ""
    url = "https://fhir.alliance4u.io/api/observation"
    context = {}
    if request.method == 'POST':
        poids = int(request.POST['poids'])
        taille = int(request.POST['taille'])
        date = request.POST['date-heure']
        date_stripped = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
        date_aware = timezone.make_aware( date_stripped, timezone.get_current_timezone()).isoformat()
        context = {"date": date_aware}
        headers = {}
        payloadWeight = {
  "resourceType" : "Observation",
  "id": "217215f1",
  "meta" : {
    "profile" : [
      "http://hl7.org/fhir/us/vitals/StructureDefinition/body-weight"
    ]
  },
  "text" : {
    "status" : "extensions",
    "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: Observation</b><a name=\"bodyWeight-example\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource Observation &quot;bodyWeight-example&quot; </p><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-body-weight.html\">Body Weight</a></p></div><p><b>Device Code</b>: Floor scale, electronic <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://browser.ihtsdotools.org/\">SNOMED CT</a>#469204003)</span></p><p><b>Associated Situation</b>: Undressed <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://browser.ihtsdotools.org/\">SNOMED CT</a>#248160001)</span></p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"http://terminology.hl7.org/5.0.0/CodeSystem-observation-category.html\">Observation Category Codes</a>#vital-signs)</span></p><p><b>code</b>: Body weight <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://loinc.org/\">LOINC</a>#29463-7)</span></p><p><b>subject</b>: <span>: Small Child1234</span></p><p><b>encounter</b>: <span>: GP Visit</span></p><p><b>effective</b>: 2019-10-16 12:12:29-0900</p><p><b>value</b>: 25 kg<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code kg = 'kg')</span></p></div>"
  },
  "extension" : [
    {
      "url" : "http://hl7.org/fhir/StructureDefinition/observation-deviceCode",
      "valueCodeableConcept" : {
        "coding" : [
          {
            "system" : "http://snomed.info/sct",
            "code" : "469204003",
            "display" : "Floor scale, electronic"
          }
        ]
      }
    },
    {
      "url" : "http://hl7.org/fhir/us/vitals/StructureDefinition/AssociatedSituationExt",
      "valueCodeableConcept" : {
        "coding" : [
          {
            "system" : "http://snomed.info/sct",
            "code" : "248160001",
            "display" : "Undressed"
          }
        ]
      }
    }
  ],
  "status" : "final",
  "category" : [
    {
      "coding" : [
        {
          "system" : "http://terminology.hl7.org/CodeSystem/observation-category",
          "code" : "vital-signs",
          "display" : "Vital Signs"
        }
      ],
      "text" : "Vital Signs"
    }
  ],
  "code" : {
    "coding" : [
      {
        "system" : "http://loinc.org",
        "code" : "29463-7"
      }
    ],
    "text" : "Body weight"
  },
  "subject" : {
    "reference":"Patient/66df16de99cb8a001240f329", #TODO remplacer ce champs par "Patient/<id_du_patient_connecté>"
    "display" : "Ringuet" #TODO : récupérer le nom du patient connecté à l'application
  },
  "encounter" : {
    "display" : "GP Visit"
  },
  "effectiveDateTime" : date_aware  , #TODO convertir cette date en date conforme au format ISOx
  "valueQuantity" : {
    "value" : poids,
    "unit" : "kg",
    "system" : "http://unitsofmeasure.org",
    "code" : "kg"
  }
}
    
        payloadHeight= { 
  "resourceType" : "Observation",
  
  "id" : "217215f2",
  "meta" : {
    "profile" : [
      "http://hl7.org/fhir/us/vitals/StructureDefinition/height"
    ]
  },
  "text" : {
    "status" : "extensions",
    "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative: Observation</b><a name=\"height-example\"> </a></p><div style=\"display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%\"><p style=\"margin-bottom: 0px\">Resource Observation &quot;height-example&quot; </p><p style=\"margin-bottom: 0px\">Profile: <a href=\"StructureDefinition-height.html\">Body Height</a></p></div><p><b>Device Code</b>: Measuring tape <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://browser.ihtsdotools.org/\">SNOMED CT</a>#51791000)</span></p><p><b>status</b>: final</p><p><b>category</b>: Vital Signs <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"http://terminology.hl7.org/5.0.0/CodeSystem-observation-category.html\">Observation Category Codes</a>#vital-signs)</span></p><p><b>code</b>: Body height <span style=\"background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki\"> (<a href=\"https://loinc.org/\">LOINC</a>#8302-2)</span></p><p><b>subject</b>: <span>: Small Child1234</span></p><p><b>encounter</b>: <span>: GP Visit</span></p><p><b>effective</b>: 2019-10-16 12:12:29-0900</p><p><b>value</b>: 102 cm<span style=\"background: LightGoldenRodYellow\"> (Details: UCUM code cm = 'cm')</span></p></div>"
  },
  "extension" : [
    {
      "url" : "http://hl7.org/fhir/StructureDefinition/observation-deviceCode",
      "valueCodeableConcept" : {
        "coding" : [
          {
            "system" : "http://snomed.info/sct",
            "code" : "51791000",
            "display" : "Measuring tape"
          }
        ]
      }
    }
  ],
  "status" : "final",
  "category" : [
    {
      "coding" : [
        {
          "system" : "http://terminology.hl7.org/CodeSystem/observation-category",
          "code" : "vital-signs",
          "display" : "Vital Signs"
        }
      ],
      "text" : "Vital Signs"
    }
  ],
  "code" : {
    "coding" : [
      {
        "system" : "http://loinc.org",
        "code" : "8302-2",
        "display" : "Body height"
      }
    ]
  },
  "subject" : {
    "reference":"Patient/66df16de99cb8a001240f329",
    "display" : "Dominique"
  },
  "encounter" : {
    "display" : "GP Visit"
  },
  "effectiveDateTime" : date_aware,
  "valueQuantity" : {
    "value" : taille,
    "unit" : "cm",
    "system" : "http://unitsofmeasure.org",
    "code" : "cm"
  }
}    
    responseWeight = requests.post(url, json=payloadWeight,headers=headers)
    if responseWeight.status_code == 200:
        retour_reponse = responseWeight.text
    else:
        print('erreur lors de lenvoi des données', responseWeight.status_code, responseWeight.text)
    
    responseHeight = requests.post(url, json=payloadHeight, headers= headers) 
    if responseHeight.status_code == 200:
        retour_reponse += responseHeight.text
    else:
        print('erreur lors de lenvoi des données', responseHeight.status_code, responseHeight.text)    


    context= {"reponse" : retour_reponse, "date" : date_aware}
    

    return render(request,'app_fhir/envoi_observations.html',context )   
   
   
   
   
   
   
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
             pass           
    else:

        form = AuthenticationForm()
    return render(request, 'app_fhir/connexion.html', {'form': form})