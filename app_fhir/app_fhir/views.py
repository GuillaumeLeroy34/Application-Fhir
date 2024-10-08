from django.shortcuts import render, redirect 
import requests
from django.utils import timezone
from datetime import datetime as dt
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import Patient
import json
import traceback
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    username = request.user.username
    return render(request, 'app_fhir/accueil.html', {'data': data, "username" : username })

#ID médecin f011 f010
   
#post une observation: observer la doc, ne pas oublier d'inclure l'identifiant du patient connecté
@login_required
def envoi_observations(request):
  envoi = False
  weightBool = False
  heightBool = False
  payloadWeight= {} #pour une raison qui m'échappe django veut absolument que tout soit déclaré en début de fonction
  payloadHeight = {}
  headers = {}
  retour_reponse = ""
  date_aware = ""
  url = "https://fhir.alliance4u.io/api/observation"
  context = {}
  if request.method == 'POST':
      envoi = True
       #booleen pour déterminer si les deux envois ont réussi
        
      poids = int(request.POST['poids'])
      taille = int(request.POST['taille'])
      date = request.POST['date-heure']
      date_stripped = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
      date_aware = timezone.make_aware( date_stripped, timezone.get_current_timezone()).isoformat()
      context = {"date": date_aware}
      headers = {}
      payloadWeight = {
"resourceType" : "Observation",
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
  "reference":"Patient/{id}".format(id=request.user.patientId), #TODO remplacer ce champs par "Patient/<id_du_patient_connecté>"
  "display" : request.user.last_name #TODO : récupérer le nom du patient connecté à l'application
},
"encounter" : {
  "display" : "GP Visit"
},
"effectiveDateTime" : date_aware  , 
"valueQuantity" : {
  "value" : poids,
  "unit" : "kg",
  "system" : "http://unitsofmeasure.org",
  "code" : "kg"
}
}
  
      payloadHeight= { 
"resourceType" : "Observation",


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
  "reference":"Patient/{id}".format(id=request.user.patientId),
  "display" : request.user.last_name
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
    weightBool = True
    retour_reponse = responseWeight.text
  else:
    print('erreur lors de lenvoi des données', responseWeight.status_code, responseWeight.text)
  
  responseHeight = requests.post(url, json=payloadHeight, headers= headers) 
  if responseHeight.status_code == 200:
    heightBool = True
    retour_reponse += responseHeight.text
  else:
      print('erreur lors de lenvoi des données', responseHeight.status_code, responseHeight.text)    


  context= {"reponse" : weightBool & heightBool , "date" : date_aware}
  

  return render(request,'app_fhir/envoi_observations.html',context )   
  
  
   
def navigation(request):
    return render(request, 'app_fhir/navigation.html')
  
 
  

def register(request):
    url = 'https://fhir.alliance4u.io/api/patient'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            date_naissance = form.cleaned_data.get('date_naissance')
            password = form.cleaned_data.get('password1') 
            payload = {
              "resourceType": "Patient",

              "name": [
                {
                  "use": "official",
                  "family": last_name,
                  "given": [
                    first_name
                  ]
                },
              ],
              'gender': 'male' if form.cleaned_data.get('genre') == 'Male' else 'female',
              "birthDate": str(date_naissance)  
            }
            try :
              response = requests.post(url,json = payload)
              print(response.text)
              response_data = response.json()
              if response.status_code == 200 and 'id' in response_data:
                patientId = response_data['id']
              
                user = Patient.objects.create_user(
                            username=username,
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            date_naissance=date_naissance,
                            patientId=patientId,  # Use the patientId from the external API
                            password=password  # Create the user with the password
                        )
                user.save()
                user = authenticate(username=username, password=password)
                if user is not None:
                  login(request, user)
              else:
                      form.add_error(None, 'Failed to create patient. Please try again.')
                    
            except requests.RequestException as e: 
              form.add_error(None, 'An error occurred while contacting the external API.')
              print(f"API Error: {e}")
              
            return redirect('accueil')  
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'app_fhir/inscription.html', {'form': form})
   
   
   
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
              login(request, user)
              return redirect('observations')     
    else:

        form = AuthenticationForm()
    return render(request, 'app_fhir/connexion.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accueil')


def navigation(request):
    return render(request, 'app_fhir/navigation.html')
  
  
def get_bmi_data(request):
  url = "https://fhir.alliance4u.io/api/observation"  
      # Effectuer la requête GET vers l'API
  try:
      response = requests.get(url)
      response.raise_for_status()  # Vérifie si la requête a échoué
      data = response.json()  # Récupérer les données sous forme de JSON
      target_patient_id = request.user.patientId
      filtered_observations = [
        observation for observation in data 
        if observation.get("subject", {}).get("reference") == "Patient/{id}".format(id = target_patient_id)
      ]
      if filtered_observations:
        
        print(f"Found {len(filtered_observations)} observations for the patient {target_patient_id}:")  

        bmi_data = {
        "dates": [],
        "values": []
    }
        #parcourir la liste filtrée
        for observation in filtered_observations: 
          codes = observation.get("code",{}).get("coding",[])
          for code in codes:
            if code.get("code") == "39156-5":
              value_quantity =  observation.get("valueQuantity",{})
              value = value_quantity.get("value","Na")
              unit = value_quantity.get("unit","Na")
              effective_date = observation.get("effectiveDateTime")
              if value is not None and effective_date is not None:
                effective_date = dt.fromisoformat(effective_date.replace("Z","+00:00"))
                bmi_data["dates"].append(effective_date.strftime("%Y-%m-%d %H:%M"))
              bmi_data["values"].append(observation["valueQuantity"]["value"])

      else:
          print(f"No observations found for the patient {target_patient_id}")      
  except requests.exceptions.HTTPError as err:
    print("erreur http")
    traceback.print_exc()
  except Exception as err:
      print("une erreur est survenue; traceback")
      traceback.print_exc() 
  zipped_data = list(zip(
      [dt.strptime(date, "%Y-%m-%d %H:%M") for date in bmi_data["dates"]],
      bmi_data["values"]
  ))

  # Step 2: Sort the zipped list by the datetime objects
  sorted_data = sorted(zipped_data, key=lambda x: x[0])

  # Step 3: Unzip the sorted list back into dates and values
  sorted_dates, sorted_values = zip(*sorted_data)

  # Step 4: Update the original data structure with the sorted values
  # Convert datetime objects back to "YYYY-MM-DD HH:MM" format
  bmi_data["dates"] = [date.strftime("%Y-%m-%d %H:%M") for date in sorted_dates]
  bmi_data["values"] = list(sorted_values)
  return(JsonResponse(bmi_data))    
      
def graphique_observation(request):
  url = "https://fhir.alliance4u.io/api/observation"  
    # Effectuer la requête GET vers l'API
  try:
      response = requests.get(url)
      response.raise_for_status()  # Vérifie si la requête a échoué
      data = response.json()  # Récupérer les données sous forme de JSON
      data_text = response.text
      target_patient_id = request.user.patientId
      filtered_observations = [
        observation for observation in data 
        if observation.get("subject", {}).get("reference") == "Patient/66e061a899cb8a001240f383"
      ]
      if filtered_observations:
        
        print(f"Found {len(filtered_observations)} observations for the patient {target_patient_id}:")  

        bmi_data = {
        "dates": [],
        "values": []
    }
        #parcourir la liste filtrée
        for observation in filtered_observations: 
          codes = observation.get("code",{}).get("coding",[])
          for code in codes:
             if code.get("code") == "39156-5":
               value_quantity =  observation.get("valueQuantity",{})
               value = value_quantity.get("value","Na")
               effective_date = observation.get("effectiveDateTime")
               if value is not None and effective_date is not None:
                 effective_date = datetime.fromisoformat(effective_date.replace("Z","+00:00"))
                 bmi_data["dates"].append(effective_date.strftime("%Y-%m-%d %H:%M"))
               bmi_data["values"].append(observation["valueQuantity"]["value"])

          
        
          
          #ajouter les informations extraites à une liste de sortie
      else:
          print(f"No observations found for the patient {target_patient_id}")
      if bmi_data:
        print("la liste traitée fait {taille} éléments".format(taille = len(bmi_data)))
      
  except requests.exceptions.HTTPError as err:
    print("erreur http")
    traceback.print_exc()
  except Exception as err:
      print("une erreur est survenue; traceback")
      traceback.print_exc()
      

  
  return render(request, 'app_fhir/graphique_observations.html', { "observations" : bmi_data, "nom" : request.user.last_name, "prenom" : request.user.first_name })

  
  

@login_required
def bmi_chart_view(request):
  url = "https://fhir.alliance4u.io/api/nutrition-order"
  payload =  {
    "resourceType": "NutritionOrder",
    "subject": {
      "reference": "Patient/66e061a899cb8a001240f383"
    },
    "dateTime": "2024-09-13",
    "orderer": {
      "reference": "Practitioner/f016"
    },
    "oralDiet": {
      "type": [
        {
          "text": "Régime hypercalorique"
        }
      ],
      "schedule": {},
      "instruction": "bro stop le bk tous les jours"
    },
    "supplement": []
  }
  try:
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()  # Récupérer les données sous forme de JSON
    target_patient_id = request.user.patientId
    filtered_nutrition_orders = [
      order for order in data 
      if order.get("subject", {}).get("reference") == "Patient/{id}".format(id = target_patient_id)
    ]
    print(filtered_nutrition_orders)
    notesItems = []
    for order in filtered_nutrition_orders: 
      datetime = order.get("dateTime",)
      diet = order.get("oralDiet",{}).get("type")[0].get("text")
      instructions = order.get("oralDiet").get("instruction")
      nomPraticien = ""
      prenomPraticien = ""
      try:
        practitionerId = order.get("orderer").get("reference").split('/')[-1]
        practitionerResponse = requests.get("https://fhir.alliance4u.io/api/practitioner/{id}".format(id=practitionerId))
        practitioner = practitionerResponse.json()
        nomPraticien = practitioner.get("name")[0].get("family")
        prenomPraticien = practitioner.get("name")[0].get("given")[0]
      except Exception as e:
        print("an error has occured")
        traceback.print_exc()
      
      
      notesItems.append({"datetime": datetime,
                         "diet" : diet, 
                         "instructions" : instructions, 
                         "nomPraticien": nomPraticien,
                         "prenomPraticien": prenomPraticien})

  except Exception as e:
    print("une erreur est survenue")
    traceback.print_exc()
    
    
    
  return render(request, 'app_fhir/bmichart.html',{"notesItems" : notesItems})
  
  
@login_required
def compte(request):
  if request.method == "POST":
    print("la methode est")
    if 'confirm' in request.POST:
      print("confirm vrai")
      url = "https://fhir.alliance4u.io/api/patient/{idpatient}".format(idpatient = request.user.patientId)
      try:
        requests.delete(url)
      except Exception as err:
        print('une erreur est survenue')
        traceback.print_exc()
      request.user.delete()
      messages.success(request, 'User has been deleted successfully.')
      return redirect('/')
  else:
    return render(request,"app_fhir/compte.html", {"nom" : request.user.first_name, "prenom" : request.user.last_name}) 
  
