# Compte-rendu du projet 8 - Purbeurre

## Liens utiles

*  [site hébergé sur heroku](http://remace-purbeurre.herokuapp.com) 

*  [github](https://github.com/remace/OC-P8-Purbeurre)

*  [trello](https://trello.com/b/MMPgH3xg/p8-openfoodfacts) 

*  [copie du Trello sur github](https://github.com/remace/OC-P8-Purbeurre/projects/1) 

## Démarche de conception

j'ai commencé par installer django puis créer la page d'accueil du site. ensuite je me suis attelé à la conception du module d'authentification, et enfin j'ai travaillé sur les module qui concerne les produits.

pour les deux dernières étapes, j'ai procédé de la manière suivante:

* créer un objet simple dans le modèle, puis une vie pour chaque fonctionnalité liée à ce modèle, et le template associé. une fois tout ceci fonctionnel, j'ai étoffé petit à petit le modèle pour couvrir les besoins de chaque vue et template. par exemple, pour les produits:
  
  * j'ai commencé par créer un modèle de produit avec seulement un nom, une catégorie et un identifiant (automatique fourni par django)
  
  * j'ai créé un script minimal pour importer quelques produits de quelques catégories depuis la base de données
  
  * j'ai ensuite créé les vues et le template liées à ce modèle (vue de présentation des résultats de recherche, qui sert aussi pour la présentation de la liste des favoris, et pour la présentation des résultats de recherche d'alternatives)
  
  * ensuite j'ai rajouté au modèle les données nutritionnelles, et créé la vue et le template de présentation des détails du produit
  
  * même idée pour les photos des produits

 <div style="page-break-after: always;"></div>

## Test Driven Development

tout au long du projet, J'ai utilisé une politique de développement par les tests, mais j'ai fait plusieurs essais:

j'ai d'abord considéré coder un seul test, de toute la feature, puis apporter le changement dans le code pour qu'il soit validé, avec les effets suivants:

* test plus facile et plus rapide à créer

* manque de visibilité sur la feature globale, ce qui m'a amené à faire de gros changements pour adapter le code aux derniers tests

j'ai ensuite essayé le contraire: écrire tous les tests unitaires d'une fonctionnalité d'abord, puis coder la vue au complet.

* meilleure vue d'ensemble au moment de coder la fonctionnalité, 

## Difficultés rencontrées

j'ai eu des difficultés à adapter le thème fourni, notamment à propos de l'alignement des balises entre elles

j'ai aussi et des difficultés à parcourir la base de données d'Open Food Facts, dans laquelle les données sont peu normalisées: il manque certaines données, d'autres sont dupliquées... j'ai fini par donner des valeurs "impossibles" par défaut, et à modifier leur rendu dans le template associé. par exemple, pour les quantités nutritionnelles, j'ai mis -1 pour les données non-renseignées, et j'affiche "N/A" dans le tempate.












