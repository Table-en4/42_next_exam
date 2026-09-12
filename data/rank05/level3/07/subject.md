Write a function that computes the length of the shortest transformation sequence from a `start` word to an `end` word using a dictionary list of allowed words `sentence`.

Each transformation step must change exactly one single character. All intermediate words must exist in `sentence`.

The function should:
- Return the total number of words in the shortest ladder (including `start` and `end`).
- Return 0 if no transformation sequence is possible.