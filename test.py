import numpy as np
from hadamard import Hadarmard

h = Hadarmard(2)
print(h.R,'\n')
#print(h.cobordes[0],'\n')
#print(h.cobordes[2],'\n')
#print(h.cobordes[3])
print(np.multiply(np.multiply(h.cobordes[0],h.cobordes[2]),h.cobordes[3]))
