Écris deux fonctions : `compress` et `decompress`.

`compress(s: str) -> str` :
- Compresse les caractères consécutifs répétés en ajoutant leur nombre après le caractère.
- Omets le nombre '1' pour un caractère unique.
- Renvoie une chaîne vide si l'entrée est vide.

`decompress(s: str) -> str` :
- Décompresse une chaîne compressée vers sa forme initiale.
- Gère les nombres à plusieurs chiffres (ex. "a12" -> 12 'a').