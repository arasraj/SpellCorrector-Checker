import sys
from collections import defaultdict
from collections import namedtuple

class PhoneticSuggestor():
  """An implementation of the Soundex algorithm """
  
  def __init__(self, src):
    self.rules = {}
    self.word_src = src
    self.phonetic_index = defaultdict(list)


  def encode(self, word):
    word = word.lower()
    encoding = [word[0]]

    tmp = []
    for char in word[1:]:
      if char in self.rules:
        tmp.append(self.rules[char])

    for i in range(len(tmp)-1, 0, -1):
      if tmp[i] == tmp[i-1]:
        tmp.pop(i)

    encoding += tmp
    padding = 4-len(encoding)
    if padding > 0:
      for i in range(padding):
        encoding.append(0)

    return ''.join(map(str, encoding[:4]))

  def word_frequencies(self):
    """Returns a dict of words -> freq """

    word_freq = {}
    for line in open('word_freq.txt', 'rt'):
      line = line.rstrip('\n').lower()
      line = line.split()
      word_freq[line[0]] = int(line[1])
    return word_freq

  def index(self):
    WordFreq = namedtuple('WordFreq', ['word', 'freq'])
    word_freq = self.word_frequencies()
    for word in open(self.word_src, 'rt'):
      word = word.rstrip('\n').lower()
      encoding = self.encode(word)
      freq = 0
      if word in word_freq:
      	freq = word_freq[word]
      self.phonetic_index[encoding].append(WordFreq(word, freq))

  def suggest(self, word):
    encoding = self.encode(word.lower())
    suggestions = self.phonetic_index[encoding]

    # gets all candidates for encoded word and sorts by english frequency
    return [suggestion.word 
            for suggestion in 
            sorted(suggestions, key=lambda suggest: suggest.freq, 
            reverse=True)][:10]

  def init_rules(self):
    self.rules['b'] = 1
    self.rules['f'] = 1
    self.rules['p'] = 1
    self.rules['v'] = 1

    self.rules['c'] = 2
    self.rules['g'] = 2
    self.rules['j'] = 2
    self.rules['k'] = 2
    self.rules['s'] = 2
    self.rules['x'] = 2
    self.rules['z'] = 2

    self.rules['d'] = 3
    self.rules['t'] = 3
    
    self.rules['l'] = 4

    self.rules['m'] = 5
    self.rules['n'] = 5

    self.rules['r'] = 6

if __name__ == '__main__':
  words_src = sys.argv[1]
  word = sys.argv[2]
  suggestor = PhoneticSuggestor(words_src)
  suggestor.init_rules()
  suggestor.index()
  print suggestor.suggest(word)
