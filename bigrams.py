from collections import defaultdict
from collections import namedtuple
import sys

class BigramSpellSuggestor():
  """Offers spelling suggestions comparing the source word with 
     candidate suggestion words using jaccard similarity of bigram
     intersections. Suggested words are then sorted according to 
     there frequency.
  """

  def __init__(self, src):
    self.word_source = src
    self.bigrams = defaultdict(list)
    

  def index_bigrams(self):
    WordData = namedtuple('WordData', ['word', 'freq'])
    word_freq = self.word_frequencies()

    # create bigrams dict
    for word in open(self.word_source, 'rt'):
      word = word.rstrip('\n')
      for i in range(len(word)-1):
        freq = 0
        if word in word_freq:
          freq = word_freq[word]
        self.bigrams[word[i:i+2]].append(WordData(word, freq))

  def word_frequencies(self):
    """Returns a dict of words -> freq """

    word_freq = {}
    for line in open('word_freq.txt', 'rt'):
      line = line.rstrip('\n')
      line = line.split()
      word_freq[line[0]] = int(line[1])
    return word_freq

  def suggest(self, word):
    """Returns list of suggestion word """

    source_bigrams = self.word_bigrams(word)
    suggestions = set()
    num_grams = defaultdict(lambda: 0)

    # find how many bigrams suggested words contain
    for gram in source_bigrams: 
      for word in self.bigrams[gram]:
        num_grams[word] += 1

    # calculate jaccard similarity of source bigrams to suggested word bigrams.
    for candidate, intersection in num_grams.items():
      jaccard = intersection / float((len(candidate.word)-1) + len(source_bigrams) - intersection)

      if jaccard > 0.48:
        suggestions.add((candidate, jaccard))

    # sort by similarity
    suggestions = sorted(suggestions, key=lambda jaccard: jaccard[1], reverse=True)[:30]
    # sort by word freq
    suggestions = sorted(suggestions, key=lambda suggestion: suggestion[0].freq, reverse=True)[:10]
    return [suggestion[0].word for suggestion in suggestions]


  def word_bigrams(self, word):
    return set([word[i:i+2] for i in range(len(word)-1)])

if __name__ == '__main__':
	word_src = sys.argv[1]
	word = sys.argv[2]
	suggestor = BigramSpellSuggestor(word_src)
	suggestor.index_bigrams()
	print suggestor.suggest(word)

