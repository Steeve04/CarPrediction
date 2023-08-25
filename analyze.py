import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/cars.csv')
df.columns

df.head(10)

df.info()

## Voir les valeur manquantes
pd.DataFrame(df.isnull().sum())

df.describe() ## Les variables quantitatives(numériques)

df.describe(include='O') ##Les variables qualitatives(catégoriques)

df.dtypes

# Supprimer les lignes avec des valeurs manquantes avec la méthode dropna
new_df = df.dropna()

new_df['Marque'] = new_df['Model'].str.split().str[0]
new_df=new_df[['Marque','Model', 'Prix', 'Annee', 'Kilometrage', 'Boite_Vitesse', 'Energie',
       'Controle_Technique', 'Premiere Main', 'Portes', 'Places', 'Puissance']]

annee=df['Annee'].value_counts()
annee

plt.bar(annee.index, annee.values)
plt.xlabel('Année')
plt.ylabel('Nombre d\'occurrences')
plt.title('Diagramme de comptage des années')
plt.xticks(rotation=45)  # Rotation des étiquettes d'année pour une meilleure lisibilité
plt.show()

annee=new_df['Annee'].value_counts()
colors = plt.cm.viridis(annee.index / max(annee.index))
plt.bar(annee.index, annee.values, color=colors)
plt.xlabel('Année')
plt.ylabel('Nombre de voiture')
plt.title('Diagramme de comptage des années')
plt.xticks(rotation=45)  # Rotation des étiquettes d'année pour une meilleure lisibilité
plt.show()

sns.set(style="darkgrid")
km=new_df['Kilometrage'].value_counts()

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Kilometrage', kde=True, palette='viridis')# in the next version of the distplot function, one would have to write:
# sns.distplot(data=df, x="sepal_length", kind='hist') # note that 'kind' is 'hist' by default
plt.show()

prixx=pd.DataFrame(new_df['Prix'].value_counts())
prixx

plt.style.use('seaborn-darkgrid')

# Créer le tracé de ligne
plt.fill_between(prixx.index,prixx['Prix'], color="skyblue", alpha=0.3)
plt.plot( prixx.index, prixx['Prix'],color="skyblue")

# Tracé de l'estimation de densité kernel (KDE)
sns.kdeplot(data=prixx['Prix'], color="orange", linewidth=2)

plt.xlabel('Prix')
plt.ylabel('Nombre de voiture')
plt.title('Nombre de voiture en fonctio de Prix')
plt.xticks(rotation=45)
plt.show()

marque=new_df['Marque'].value_counts()
plt.figure(figsize=(20, 10))
plt.bar(marque.index, marque.values, color='r')
plt.xlabel('Marque')
plt.ylabel('Nombre de voiture')
plt.title('Diagramme de nombre de voiture en fonction de la marque')
plt.xticks(rotation=45)  # Rotation des étiquettes d'année pour une meilleure lisibilité
plt.show()

modele=new_df['Energie'].value_counts()
plt.figure(figsize=(15, 10))
plt.barh(modele.index, modele.values, color='b')
plt.ylabel('Energie')
plt.xlabel('Nombre de voiture')
plt.title('Diagramme de nombre de voiture en fonction d energie')
plt.xticks(rotation=45)  # Rotation des étiquettes d'année pour une meilleure lisibilité
plt.show()
