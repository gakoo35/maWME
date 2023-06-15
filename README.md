# Projet MA_WME - Airline sentiment analysis



## Introduction

Ce projet rentre dans le cadre du cours Master HES-SO MA-WEM. Il a pour but de mettre en pratique les différentes notions de "web scrapping" que nous avons vu en classe pour récupérer des données sur le web. Une fois les données récupérées et nettoyées, elles pourront être utilisées pour entrainer des algorithmes de Machine Learning de sorte à mettre en lumière des statistiques liées à ces données. Un travail de visualisation complètera ce projet. Il présentera les diverses statistiques extraites de nos modèles.
Autrement dit, l'objectif général du projet est donc de récupérer des données depuis internet afin d'en extraire une valeur "business" et de les présenter de façon lisible et compréhensible.
Nous avons tous été confronté à des désagréments (retards, pertes de bagages etc …) ou au contraire, à des bonnes surprises (sur-classement, prix de billets réduits etc…), lors de nos voyages en avion. Nous avons donc trouvé légitime de se poser la question : il y a-t-il une compagnie aérienne qui offre de meilleurs services que les autres ? Pour répondre à cette interrogation, nous avons donc décider faire de l'analyse de sentiments sur des commentaires de réseaux sociaux, liés à des compagnies aériennes. 

## File structure

- `ml` : contient le notebook qui a permit d'entraîner le modèle de machine learning qui a permis de générer les sentiments pour chaque post du dataset. 
- `scrapping` : contient les différents notebook qui ont permis de récupérer les posts reddit mais également de faire une analyse et un pre-processing pour la visualisation et le modèle ML.
- `visualization` : c'est le serveur web qui permet de visualiser les données. Il est basé sur le framework Dash de Plotly. C'est le résultat final de ce projet

## Start project

Pour utiliser le projet, il faut premièrement avoir un environnement Python fonctionnel. 

Ensuite, il faut installer les dépendances du projet. Pour cela, il faut se placer à la racine de ce projet et exécuter la commande suivante :

```bash
pip install -r requirements.txt
```

Une fois les dépendances installées, il faut se placer dans le dossier `visualization` et exécuter la commande suivante :

```bash
python index.py
```

Le serveur web est maintenant lancé. Il est accessible à l'adresse suivante : [http://localhost:8050/](http://localhost:8050/)

Les différents notebook sont également possible d'être exécutés.

## Members

- Maël Vial ( [ mael.vial@hefr.ch ](mael.vial@hefr.ch) )
- Sam Corpataux ( [ sam.corpataux@master.hes-so.ch](sam.corpataux@master.hes-so.ch) )
- Gaël Koch ( [ gael.koch@master.hes-so.ch](gael.koch@master.hes-so.ch) )
