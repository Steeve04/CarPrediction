import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

# annee minimale à prendre en compte
min_year = str(datetime.datetime.now().year - 5)

# Création des listes pour stocker les informations
brand = []
price = []
year = []
km = []
gear = []
energy = []
technicalControl = []
firstHand = []
doors = []
seats = []
ratedHorsePower = []

# Parcourt les 240 premières pages du site
for page in range(1, 241):

    # URL du site cible en filtrant sur les 5 derniéres années
    url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page="+str(page)+"&yearMin="+min_year

    # Envoie une requête GET au site
    response = requests.get(url)

    # Vérification de la requête
    if response.status_code == 200:
        print('Connexion établie sur lacentrale.fr')
        # Utiliser Beautiful Soup pour analyser la page HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Tous les éléments qui contiennent les informations des voitures
        vehicle_elements = soup.find_all("div", class_="searchCardContainer")

        # Parcourt les éléments et extraire les informations souhaitées
        for vehicle_element in vehicle_elements:
            # Extraction de la marque
            marques = vehicle_element.find("h2", class_="Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2")
            if marques is not None:
                marque = marques.text
            else:
                marque = None
            # Extraction du prix
            price_element = vehicle_element.find("span", class_="Vehiculecard_Vehiculecard_price")
            if price_element:
                prix = price_element.get_text(strip=True)
                prix = prix.replace("€", "").replace(" ", "")
            # Extraction des principales caractéristiques
            features = vehicle_element.find("div", class_="Vehiculecard_Vehiculecard_characteristics")
            if features is not None:
                features = features
                characteristics = features.find_all("div", class_="Text_Text_text")
            else:
                features = None

            # Vérification de l'existence d'au moins une caractéristique
            if len(characteristics) >= 4:
                # Séparation des principales caractéristiques
                annee = characteristics[0].text.strip()
                kilometrage = characteristics[1].text.strip().replace(" km", "").replace(" ", "")
                boite_vitesse = characteristics[2].text.strip()
                energie = characteristics[3].text.strip()
            else:
                print("Pas assez d'éléments pour extraire les caractéristiques complètes.")

            # Récupération du lien pour la voiture concernée
            a_elements = vehicle_element.find_all("a", class_="Vehiculecard_Vehiculecard_vehiculeCard")

            for a_element in a_elements:
                href_value = a_element.get("href")

            url_car = "https://www.lacentrale.fr"+href_value

            # Envoie une requête GET au site
            response_car = requests.get(url_car)

            # Vérification de la requête
            if response_car.status_code == 200:
                # Utilisation de Beautiful Soup pour analyser la page HTML
                soup = BeautifulSoup(response_car.content, "html.parser")

                # Tous les éléments qui contiennent les informations
                vehicle_info = soup.find("div", class_="GeneralInformation_grid__H0Uma")

                # Elément li avec l'ID "technicalControl"
                li_ct = vehicle_info.find('li', id='technicalControl')

                # Si l'élément li a été trouvé
                if li_ct:
                    # Extraction de l'élément span à l'intérieur de l'élément li
                    span_ct = li_ct.find('span', class_='Text_Text_text Text_Text_body1')

                    # Si l'élément span a été trouvé
                    if span_ct:
                        controleTech = span_ct.text
                    else:
                        print("Contrôle Technique non renseigné")

                # Extraction de l'élément li avec l'ID "firstHand"
                li_fh = vehicle_info.find('li', id='firstHand')

                # Si l'élément li a été trouvé
                if li_fh:
                    # Extraction de l'élément span à l'intérieur de l'élément li
                    span_fh = li_fh.find('span', class_='Text_Text_text Text_Text_body1')

                    # Si l'élément span a été trouvé
                    if span_fh:
                        premMain = span_fh.text
                    else:
                        print("Première Main non renseignée")

                # Extraction de l'élément li avec l'ID "doors"
                li_d = vehicle_info.find('li', id='doors')

                # Si l'élément li a été trouvé
                if li_d:
                    # Extraction de l'élément span à l'intérieur de l'élément li
                    span_d = li_d.find('span', class_='Text_Text_text Text_Text_body1')

                    # Si l'élément span a été trouvé
                    if span_d:
                        porte = span_d.text
                    else:
                        print("Nombre de portes non renseigné")

                # Extraction de l'élément li avec l'ID "seats"
                li_s = vehicle_info.find('li', id='seats')

                # Si l'élément li a été trouvé
                if li_s:
                    # Extraction de l'élément span à l'intérieur de l'élément li
                    span_s = li_s.find('span', class_='Text_Text_text Text_Text_body1')

                    # Si l'élément span a été trouvé
                    if span_s:
                        place = span_s.text
                    else:
                        print("Nombre de places non renseigné")

                # Extraction de l'élément li avec l'ID "ratedHorsePower"
                li_rhp = vehicle_info.find('li', id='ratedHorsePower')

                # Si l'élément li a été trouvé
                if li_rhp:
                    # Extraction de l'élément span à l'intérieur de l'élément li
                    span_rhp = li_rhp.find('span', class_='Text_Text_text Text_Text_body1')

                    # Si l'élément span a été trouvé
                    if span_rhp:
                        puissance = span_rhp.text.replace(' CV', '')
                    else:
                        print("Puissance fiscale non renseignée")

            # Ajouter les informations extraites aux listes
            brand.append(marque)
            price.append(prix)
            year.append(annee)
            km.append(kilometrage)
            gear.append(boite_vitesse)
            energy.append(energie)
            technicalControl.append(controleTech)
            firstHand.append(premMain)
            doors.append(porte)
            seats.append(place)
            ratedHorsePower.append(puissance)

        # Créer un DataFrame à partir des listes
        data = {
            "Model": brand,
            "Prix": price,
            "Annee": year,
            "Kilometrage": km,
            "Boite_Vitesse": gear,
            "Energie": energy,
            "Controle_Technique": technicalControl,
            "Premiere Main": firstHand,
            "Portes": doors,
            "Places": seats,
            "Puissance": ratedHorsePower
        }

        df = pd.DataFrame(data)
    else:
        print("La requête a échoué avec le code:", response.status_code)
