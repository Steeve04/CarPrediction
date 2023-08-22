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

        a_elements = vehicle_element.find_all("a", class_="Vehiculecard_Vehiculecard_vehiculeCard")

        for a_element in a_elements:
            href_value = a_element.get("href")

        url_car = "https://www.lacentrale.fr"+href_value

        # Envoyer une requête GET au site
        response_car = requests.get(url_car)

        # Vérifier si la requête a réussi
        if response_car.status_code == 200:
            # Utiliser Beautiful Soup pour analyser la page HTML
            soup = BeautifulSoup(response_car.content, "html.parser")
            
            # Trouver tous les éléments qui contiennent les informations
            vehicle_info = soup.find("div", class_="GeneralInformation_grid__H0Uma")

            # Trouver l'élément li avec l'ID "technicalControl"
            li_ct = vehicle_info.find('li', id='technicalControl')

            # Vérifier si l'élément li a été trouvé
            if li_ct:
                # Trouver l'élément span à l'intérieur de l'élément li
                span_ct = li_ct.find('span', class_='Text_Text_text Text_Text_body1')
                
                # Vérifier si l'élément span a été trouvé
                if span_ct:
                    technicalControl = span_ct.text
                    print("Contrôle Technique :", technicalControl)
                else:
                    print("Contrôle Technique non renseigné")

            # Trouver l'élément li avec l'ID "firstHand"
            li_fh = vehicle_info.find('li', id='firstHand')

            # Vérifier si l'élément li a été trouvé
            if li_fh:
                # Trouver l'élément span à l'intérieur de l'élément li
                span_fh = li_fh.find('span', class_='Text_Text_text Text_Text_body1')
                
                # Vérifier si l'élément span a été trouvé
                if span_fh:
                    firstHand = span_fh.text
                    print("Première Main :", firstHand)
                else:
                    print("Première Main non renseignée")
else:
    print("La requête a échoué avec le code:", response.status_code)
