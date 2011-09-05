Spell Checker and Suggestor
======

Provides various methods for spell checking and suggesting:

 1. Trie based spelling suggestor using Levenshtein dist
 2. Bloom filter based spell checker
 3. Bigram based spelling suggestor
 4. Phonetic based spelling suggestor

All methods create the required data structures necessary and then spell check/suggest.  In production, these data structures should be in memory already. 

How To Use:
--------

  For 1:

  > ./name_of_file /source/to/dictionary source_word max_distance

  For 2, 3, and 4:

  > ./name_of_file /source/to/dictionary source_word
