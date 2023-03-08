from cobordes import genera_cobordes_espacio
import numpy as np

inicio = 2
for m in genera_cobordes_espacio(3):
    print("Matriz coborde número ",inicio)
    for i in range(0,4*3):
        print(m[i])
    inicio += 1