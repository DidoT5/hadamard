import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos, construye_R, cambia_fila_i

t = 2
dos_t = t*2
cuatro_t = t*4
cobordes = genera_cobordes_espacio(t)
R = construye_R(t, dos_t, cuatro_t).copy()
coborde5 = cambia_fila_i(cobordes[3].copy(),4)
coborde6 = cambia_fila_i(cobordes[4].copy(),5)

def muestra_matriz(m):
    for i in range(0,cuatro_t):
        print(m[i])

muestra_matriz(coborde5)
muestra_matriz(coborde6)

