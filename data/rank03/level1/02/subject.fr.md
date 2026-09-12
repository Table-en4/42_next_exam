Écris une fonction qui trie une liste de chaînes avec une priorité à trois niveaux :
1. Tri principal : par longueur (croissant)
2. Tri secondaire : lexicographique (alphabétique, insensible à la casse, croissant)
3. Tri tertiaire : par nombre de voyelles (croissant, si longueur et ordre lexicographique égaux)

La fonction doit gérer :
- Chaînes vides et listes vides
- Casses mixtes (traiter comme des minuscules pour le tri)
- Caractères spéciaux (les ignorer pour compter les voyelles)

**Fonctions interdites : sorted(), list.sort()**