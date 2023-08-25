# Importation des librairies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Lecture de la source de données suite au scraping sur le site lacentrale.fr
df = pd.read_csv('/content/cars.csv')

# Affichage des 10 premières lignes
df.head(10)

# Structure
df.shape

# Type de données et valeurs nulles
df.info()

# Statistiques numériques
df.describe()

# Valeurs manquantes
df.isna().sum()

# Matrice de coréllation
sns.heatmap(df.corr(), annot=True, cmap="RdBu")
plt.show()

# Suppresion de la colonne Model
df.drop(labels='Model',axis= 1, inplace = True)

# Conversion de Boite_Vitesse en entier
uniq_bv = df['Boite_Vitesse'].unique().tolist()
dict_map_bv = {k: v for v, k in enumerate(uniq_bv)}
df['Boite_Vitesse'] = df['Boite_Vitesse'].map(dict_map_bv).astype(str).astype(int)

# Conversion de Energie en entier
uniq_e = df['Energie'].unique().tolist()
dict_map_e = {k: v for v, k in enumerate(uniq_e)}
df['Energie'] = df['Energie'].map(dict_map_e).astype(str).astype(int)

# Conversion de Controle_Technique en entier
uniq_ct = df['Controle_Technique'].unique().tolist()
dict_map_ct = {k: v for v, k in enumerate(uniq_ct)}
df['Controle_Technique'] = df['Controle_Technique'].map(dict_map_ct).astype(str).astype(int)

# Conversion de Premiere Main en entier
uniq_pm = df['Premiere Main'].unique().tolist()
dict_map_pm = {k: v for v, k in enumerate(uniq_pm)}
df['Premiere Main'] = df['Premiere Main'].map(dict_map_pm).astype(str).astype(int)

# Séparation de la variable cible et de ses caractéristiques
y = df['Prix']
X = df.drop('Prix',axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
print("x train: ",X_train.shape)
print("x test: ",X_test.shape)
print("y train: ",y_train.shape)
print("y test: ",y_test.shape)

CV = []
R2_train = []
R2_test = []

def prediction_model(model,model_name):
    # Entraînement du modèle
    model.fit(X_train,y_train)

    # R2 score du dataset d'entraînement
    y_pred_train = model.predict(X_train)
    R2_train_model = r2_score(y_train,y_pred_train)
    R2_train.append(round(R2_train_model,2))

    # R2 score du dataset de test
    y_pred_test = model.predict(X_test)
    R2_test_model = r2_score(y_test,y_pred_test)
    R2_test.append(round(R2_test_model,2))

    # R2 score moyen du dataset d'entraînement en utilisant la validation croisée
    cross_val = cross_val_score(model ,X_train ,y_train ,cv=5)
    cv_mean = cross_val.mean()
    CV.append(round(cv_mean,2))

    # Affichage des résultats
    print("Train R2-score :",round(R2_train_model,2))
    print("Test R2-score :",round(R2_test_model,2))
    print("Train CV scores :",cross_val)
    print("Train CV mean :",round(cv_mean,2))

    # Graphique résiduel des données d'entraînement
    fig, ax = plt.subplots(1,2,figsize = (10,4))
    ax[0].set_title('Graphique résiduel des données d\'entraînement')
    #sns.distplot((y_train-y_pred_train),hist = False,ax = ax[0])
    sns.histplot(data=y_train-y_pred_train, ax = ax[0], kde=True)
    ax[0].set_xlabel('y_train - y_pred_train')

    # Diagramme de dispersion Y_test vs Y_train
    ax[1].set_title('y_test vs y_pred_test')
    ax[1].scatter(x = y_test, y = y_pred_test)
    ax[1].set_xlabel('y_test')
    ax[1].set_ylabel('y_pred_test')

    plt.show()

###### Modèle Régression Linéaire ######
lr = LinearRegression()

# Entraînement du modèle
prediction_model(lr,"Linear_regressor.pkl")

###### Modèle Régression Ridge ######
rg = Ridge()

# Vecteur alpha avec 14 valeurs qui varient entre 10^-3 (0.001) et 10^3 (1000) en échelle logarithmique
alpha = np.logspace(-3,3,num=14)

# Meilleur estimateur de l'hyperparamètre
rg_rs = RandomizedSearchCV(estimator = rg, param_distributions = dict(alpha=alpha))

# Entraînement du modèle
prediction_model(rg_rs,"ridge.pkl")

###### Modèle Régression Lasso ######
# Création d'un objet du modèle Lasso
ls = Lasso()

# Vecteur alpha avec 14 valeurs qui varient entre 10^-3 (0.001) et 10^3 (1000) en échelle logarithmique
alpha = np.logspace(-3,3,num=14) # range for alpha

# Meilleur estimateur des hyperparamètres
ls_rs = RandomizedSearchCV(estimator = ls, param_distributions = dict(alpha=alpha))

# Entraînement du modèle
prediction_model(ls_rs,"lasso.pkl")

###### Modèle Forêt Aléatoire ######
rf = RandomForestRegressor()

# Nombre d'arbres dans la Forêt aléatoire
n_estimators=list(range(500,1000,100))

# Nombre maximal de niveaux dans l'arbre
max_depth=list(range(4,9,4))

# Nombre minimum d'échantillons pour diviser un noeud interne
min_samples_split=list(range(4,9,2))

# Nombre minimum d'échantillons requis pour être à un noeud feuille
min_samples_leaf=[1,2,5,7]

# Nombre de caractéristiques pour chaque fractionnement
max_features=['sqrt']

# Dictionnaire d'hyperparamètres
param_grid = {"n_estimators":n_estimators,
              "max_depth":max_depth,
              "min_samples_split":min_samples_split,
              "min_samples_leaf":min_samples_leaf,
              "max_features":max_features}

# Meilleur estimateur des hyperparamètres
rf_rs = RandomizedSearchCV(estimator = rf, param_distributions = param_grid)

# Entraînement du modèle
prediction_model(rf_rs,'random_forest.pkl')

###### Modèle Regression Gradient Booting ######
gb = GradientBoostingRegressor()

# Taux de correction
learning_rate = [0.001, 0.01, 0.1, 0.2]

# Nombre d'arbres Gradient boosting
n_estimators=list(range(500,1000,100))

# Nombre maximal de niveaux dans l'arbre
max_depth=list(range(4,9,4))

# Nombre minimum d'échantillons pour diviser un noeud interne
min_samples_split=list(range(4,9,2))

# Nombre minimum d'échantillons requis pour être à un noeud feuille
min_samples_leaf=[1,2,5,7]

# Nombre de caractéristiques pour chaque fractionnement
max_features=['sqrt']

# Dictionnaire d'hyperparamètres
param_grid = {"learning_rate":learning_rate,
              "n_estimators":n_estimators,
              "max_depth":max_depth,
              "min_samples_split":min_samples_split,
              "min_samples_leaf":min_samples_leaf,
              "max_features":max_features}

# Meilleur estimateur des hyperparamètres
gb_rs = RandomizedSearchCV(estimator = gb, param_distributions = param_grid)

# Entraînement du modèle
prediction_model(gb_rs,"gradient_boosting.pkl")

# Afficher les meilleurs paramètres
print(gb_rs.best_estimator_)

###### Utilisation du modèle Gradient Boosting pour la prédiction ######
# Meilleur modèle après recherche aléatoire
best_gb_model = gb_rs.best_estimator_

# Exemple d'une nouvelle voiture (données en entrée)
new_car = pd.DataFrame({
    'Annee': [2018],
    'Kilometrage': [100000],
    'Boite_Vitesse': [0],
    'Energie': [2],
    'Controle_Technique': [0],
    'Premiere Main': [0],
    'Portes': [5],
    'Places': [7],
    'Puissance': [5]
})

# Utilisation du modèle pour faire une prédiction
predicted_price = best_gb_model.predict(new_car)

# Prix arrondi en entier
rounded_price = int(round(predicted_price[0]))

# Affichage de la prédiction
print("Prix prédit:", rounded_price, "€")
