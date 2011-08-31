#!/usr/bin/env python

import murmur


class BloomFilter():
  """This is your standard Bloom Filter. It is a probabilistic data structure
     allowing constant time retrieval of whether an item is in a set or not.
     It guarantees that an item is not in the set of the bloom filter 
     returns False.  If it returns True, there is a very low probability that
     the item is not in the set.  Of course you can make this probability as
     high or low as you want by modifying how many hashes you use and how large
     your bitarray is.

     This implementation uses the python builtin bytearray as its bit array.
     The correct byte index and offset are calculated to emulate a bit array.
  """

  def __init__(self, size, numhashes):
    self.size = 2 ** size
    self.bitarray = bytearray(self.size)
    self.num_hashes = numhashes

  def insert(self, key):
    indexes = self.key_index(key)
    for index in indexes:
      byte_index = index / 8 # index into "bit" array
      byte_offset = index % 8 # bit offset 
      # set the correct bit in the bit array
      self.bitarray[byte_index] |= (2 ** byte_offset) 
  
  def key_index(self, key):
    """Returns a list of self.num_hashes (N) hashes. Instead of creating
       N different index numbers we only execute the
       Murmur hash function twice. The correct number of hashes are
       then calculated using these to hashes. The logic behind this
       is outlined here: 

       http://www.eecs.harvard.edu/~kirsch/pubs/bbbf/esa06.pdf

       Basically, you get the same distribution of hashes while saving
       on computation as opposed to calculating the hash of a key N times.
    """

    hash1 = murmur.hash(key, 0)
    hash2 = murmur.hash(key, hash1)

    indexes = [abs(hash1 + (i * hash2)) % self.size for i in range(self.num_hashes)]
    return indexes

  def check(self, key):
    """Checks if a key is in the set by calculating the N hashes
       and checking if the corresponding bit in the bit array is
       set to 1.
    """

    indexes = self.key_index(key)
    for index in indexes:
      byte_index = index / 8
      byte_offset = index % 8
      byte = self.bitarray[byte_index]
      mask = 2 ** byte_offset 
      if (byte & mask) == 0:
      	return False
    return True

class SpellChecker(BloomFilter):
  def __init__(self, size, numhashes, words_src):
    self.words_src = words_src
    BloomFilter.__init__(self, size, numhashes)
    self.insert_words()

  def insert_words(self):
    words = [word[:-1].lower() for word in open(self.words_src, 'rt')]
    for word in words:
    	self.insert(word)


if __name__ == '__main__':
	sc = SpellChecker(20, 5, '/usr/share/dict/words')
	print sc.check('bob')
	print sc.check('business')
	print sc.check('thwis')
