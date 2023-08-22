import requests
from bs4 import BeautifulSoup
import datetime

min_year = str(datetime.datetime.now().year - 5)

# URL du site cible en filtrant sur les 5 derniéres années
url = "https://www.lacentrale.fr/listing?yearMin="+min_year

# Envoyer une requête GET au site
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    print('Connexion établie sur lacentrale.fr')
    # Utiliser Beautiful Soup pour analyser la page HTML
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Trouver tous les éléments qui contiennent les informations
    vehicle_elements = soup.find_all("div", class_="searchCardContainer")
    
    # Parcourir les éléments et extraire les informations souhaitées
    for vehicle_element in vehicle_elements:
        #image = vehicle_element.find("img")["src"]
        marques = vehicle_element.find("h2", class_="Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2")
        if marques is not None:
            marque = marques.text
        else:
            marque = None
        price_element = vehicle_element.find("span", class_="Vehiculecard_Vehiculecard_price")
        if price_element:
            price = price_element.get_text(strip=True)
            price = price.replace("€", "").replace(" ", "")
        features = vehicle_element.find("div", class_="Vehiculecard_Vehiculecard_characteristics")
        if features is not None:
            features = features
            characteristics = features.find_all("div", class_="Text_Text_text")
        else:
            features = None

        print("Marque:", marque)
        print("Prix:", price)
    
        if len(characteristics) >= 4:
            annee = characteristics[0].text.strip()
            kilometrage = characteristics[1].text.strip().replace(" km", "").replace(" ", "")
            boite_vitesse = characteristics[2].text.strip()
            energie = characteristics[3].text.strip()

            print("Année:", annee)
            print("Kilométrage:", kilometrage)
            print("Boîte de vitesse:", boite_vitesse)
            print("Énergie:", energie)
        else:
            print("Pas assez d'éléments pour extraire les caractéristiques complètes.")
else:
    print("La requête a échoué avec le code:", response.status_code)
