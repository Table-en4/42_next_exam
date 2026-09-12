Écris une fonction qui détermine un ordre d'installation valide des paquets en résolvant les dépendances. Utilise le tri topologique pour t'assurer que les dépendances sont installées avant les paquets qui les requièrent.

La fonction doit :
- Prendre un dictionnaire dont les clés sont les noms de paquets et les valeurs des listes de dépendances
- Renvoyer les paquets dans l'ordre d'installation (les dépendances en premier)
- Renvoyer une liste vide si aucun ordre valide n'existe (dépendances circulaires)
- Gérer les entrées vides et les chaînes de dépendances isolées
- Ignorer les références à des paquets absents du dictionnaire d'entrée