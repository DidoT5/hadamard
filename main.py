from cobordes import genera_cobordes_espacio
import numpy as np
from caminos import multiplica_matriz_punto_por_punto

t = 3
cobordes = genera_cobordes_espacio(t).copy()
mult = multiplica_matriz_punto_por_punto(cobordes[0].copy(), 1, cobordes[1].copy(), 2, 4*t)

def muestra_matriz(m, t):
    for i in range(0,4*t):
        print(m[i])