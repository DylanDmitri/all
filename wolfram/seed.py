from random import choice

def seed(width=60):
 s = [choice((True, False)) for _ in range(width)]
 r = ['b']
 counter = 0
 for _ in range(int(width*1.5)):
  new = choice('ob')
  if new == r[-1]:
   counter += 1
  else:
   if counter>1:
    r.append(str(counter))
   counter = 0
   r.append(new)
 #r.append(str(counter))
 return ''.join(r) + '!'

import sys
if __name__=='__main__':
 print(seed(int(sys.argv[1])))
