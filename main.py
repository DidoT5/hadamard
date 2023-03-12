import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos, construye_R, calcula_numero_caminos_e_intersecciones, cambia_fila_i

t = 2
dos_t = t*2
cuatro_t = t*4
cobordes = genera_cobordes_espacio(t)
R = construye_R(t, dos_t, cuatro_t).copy()

def muestra_matriz(m):
    for i in range(0,cuatro_t):
        print(m[i])
        
print(clasifica_caminos(cobordes, 1, t))

