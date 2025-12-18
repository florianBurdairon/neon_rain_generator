# Neon Rain Generator

Ce programme python permet de générer des GIF d'étoiles filantes colorées.

## Organisation du code

Le code est réparti sur deux fichiers :
- `main.py` : qui permet de lancer l'exécution et de régler les paramètres de génération.
- `neon_rain_generator_v3.py` : qui contient l'ensemble des fonctions nécessaire pour la génération.

## Détails des paramètres

La génération des GIF est paramétrable :
- `width` et `height` permettent de régler la taille du GIF en sortie
- `num_stars` permet de régler le nombre d'étoiles
- `trail_length` permet de régler la longueur des trainées
- `speed` permet de régler la vitesse d'animation
- `angle` permet de régler l'angle de déplacement
- `frames` permet de préciser le nombre de frames à générer
- `background_color` permet de choisir la couleur du fond
- `gradient_colors` permet de définir plusieurs dégradés de couleurs utilisés de manière aléatoire pour générer les étoiles et leur trainée
- `duration` permet de choisir la durée du GIF
- `open_after_creation` permet de définir si le programme doit ouvrir le fichier après la génération

> **Remarque :** Les paramètres `frames` et `duration` sont liés. La combinaison de ces deux paramètres permet de définir le taux de rafraîchissement du GIF. \
> Par exemple : pour un GIF de 300 frames durant 10 sencondes aura un taux de rafraîchissement de 30 images par secondes.
