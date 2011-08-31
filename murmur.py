from ctypes import c_int

"""Port of MurmurHash 2.0 by Ilya Sterin in Scala to Python by Raj Arasu"""

def hash(data, seed):
  data = bytearray(data)
  length = len(data)
  m = 0x5bd1e995
  r = 24

  h = seed ^ length

  len_4 = length >> 2

  for i in xrange(len_4):
    i_4 = i << 2
    k = data[i_4+3]
    k <<= 8
    k |= (data[i_4+2] & 0xff)
    k <<= 8
    k |= (data[i_4+1] & 0xff)
    k <<= 8
    k |= (data[i_4+0] & 0xff)
    k = c_int(k*m).value
    k ^= logical_rshift(k, r)
    k  = c_int(k*m).value
    h = c_int(h*m).value
    h ^= k

  len_m = len_4 << 2
  left = length - len_m

  if left:
    if left >= 3:
      h ^= int(data[length-3] << 16)
    if left >=2:
      h ^= int(data[length-2] << 8)
    if left >= 1:
      h ^= int(data[length-1])
    h = c_int(h*m).value

  h ^= logical_rshift(h, 13)
  h = c_int(h*m).value 
  h ^= logical_rshift(h, 15)

  return h


def logical_rshift(val, n):
  return val >> n if val >= 0 else (val+0x100000000) >> n


