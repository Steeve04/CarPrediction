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

annee=df['Annee'].value_counts()
annee

plt.bar(annee.index, annee.values)
plt.xlabel('Année')
plt.ylabel('Nombre d\'occurrences')
plt.title('Diagramme de comptage des années')
plt.xticks(rotation=45)  # Rotation des étiquettes d'année pour une meilleure lisibilité
plt.show()