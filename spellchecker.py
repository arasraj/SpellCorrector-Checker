import numpy
import time

def levenshtein(source,target):
  slen = len(source)+1
  tlen = len(target)+1
  m = numpy.zeros((tlen, slen))
  
  # change to using normal lists
  for j in xrange(1,tlen):
  	m[j,0] = j

  for i in xrange(1,slen):
  	m[0,i] = i

  for j,tlet in enumerate(target, start=1):
    for i,slet in enumerate(source, start=1):
      if tlet == slet:
      	m[j,i] = m[j-1,i-1]
      else:
      	m[j,i] = min(m[j-1,i-1]+1,
      	             m[j-1,i]+1,
      	             m[j,i-1]+1)

  return m[tlen-1,slen-1]

def helper(root, target):
  total = []
  for let,val in root.alpha.items():
    #m = numpy.zeros((1, len(target)+1))
    m = []
    for i in range(len(target)+1):
      m.append(i)
    row = [1]
    for i, tlet in enumerate(target, start=1):
      if tlet == let:
        row.append(m[i-1])
      else:
        # ONLY need to keep previous row at a time
        row.append(min(m[i-1]+1,
                      m[i]+1,
                      row[i-1]+1))
    trie_levenshtein(val, target, 2, row, total)
  print 'total', total

def trie_levenshtein(trie, target, currentrow, matrix, dist): 
  tlen = len(target)+1

  for k,v in trie.alpha.items():
    row = [currentrow]
    for i,tlet in enumerate(target, start=1):
      if tlet == k:
        row.append(matrix[i-1])
      else:
        # ONLY need to keep previous row at a time
        row.append(min(matrix[i-1]+1,
                      matrix[i]+1,
                      row[i-1]+1))
    
    if v.endpoint and row[-1] <= 1:
      ed = row[-1]
      dist.append((v.endpoint, ed))

    #matrix = numpy.vstack((matrix, row))
    trie_levenshtein(v, target, currentrow+1, row, dist)
  

def valid_words(target):
  l = [word[:-1] for word in open('/usr/share/dict/words', 'r') 
       if levenshtein(word[:-1],target) <= 1]
  return l


class Trie:
  def __init__(self, endpoint=None):
    self.alpha = {}
    self.endpoint = endpoint

  def insert(self, word):
    #for word in l:
    current = self
    for let in word:
      if let not in current.alpha:
        current.alpha[let] = Trie()
      current = current.alpha[let]
    current.endpoint = word

    #self.print_trie(self.alpha,0)

  def print_trie(self, alpha,n):
    for k,v in alpha.items():
      for i in range(n): print ' ',
      print k
      if v.endpoint:
      	pass
      self.print_trie(v.alpha, n+1)

  # same as above -- delete
  def recursive_print(self, root, n):
    for key,v in root.items():
      #for i in range(n): print ' ',
      print key
      self.recursive_print(v.alpha, n+1)
      	


  def find(self, word):
    current = self
    for let in word:
      if let not in current.alpha:
      	return False
      current = current.alpha[let]
    if current.endpoint == word:
      return True
    return False

def create_trie():
  trie = Trie()
  with open('/usr/share/dict/words', 'r') as f:
    for word in f.read().split():
      if word[-1] == '\n':
        trie.insert(word[:-1].lower())
      else:
        trie.insert(word.lower())
  #trie = Trie()
  #for word in ["b's", 'baby', 'babyhood', 'cat']:
  #	trie.insert(word)


  #print 'Done'
  #print trie.find('babyhood')
  #print trie.find('baby')
  #print trie.find('cat')
  #print trie.find('insertion')
  #print trie.find('given')
  #print trie.find('smallest')
  return trie

    



if __name__ == '__main__':
	#print levenshtein('kitten', 'sitting')
	#t.build(['cadet', 'apple', 'cab', 'cabbie', 'cally'])
	#t.recursive_print(t.alpha,0)
	#helper(t,'calob')
	#print t.find('cad')
	#print t.find('appl')
	#print t.find('apple')
	#print t.find('cab')
	#print t.find('acoc')
	t = create_trie()
	start = time.time()
	helper(t, 'apple')
	end = time.time()
	print end-start
