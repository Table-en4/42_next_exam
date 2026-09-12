Write two functions: `compress` and `decompress`.

`compress(s: str) -> str`:
- Takes a string and compresses consecutive repeated characters by appending the count after the character.
- If a character appears only once consecutively, omit the number '1'.
- If the input string is empty, return an empty string.

`decompress(s: str) -> str`:
- Takes a compressed string and expands it back to its uncompressed form.
- Handles multi-digit counts (e.g., "a12" -> 12 'a's).
- If no count follows a character, it counts as 1.