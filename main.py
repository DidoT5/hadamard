from cobordes import genera_cobordes_espacio
import numpy as np
from caminos import multiplica_matriz_punto_por_punto

t = 3
dos_t = t*2
cuatro_t = t*4
cobordes = genera_cobordes_espacio(t)

def construye_R(t):
    matriz_R = np.ones( (cuatro_t, cuatro_t), dtype=np.int32)
    for i in range(1,dos_t):
        matriz_R[i,(dos_t-i):dos_t] = -1 
        matriz_R[i,(cuatro_t-i):cuatro_t] = -1
    for i in range(dos_t,cuatro_t):
        matriz_R[i,(i-dos_t+1):i+1] = -1
    return matriz_R.copy()

def es_matriz_hadamard(m):
    return np.sum(m[1:cuatro_t,:])==0



def muestra_matriz(m):
    for i in range(0,cuatro_t):
        print(m[i])

operacion = multiplica_matriz_punto_por_punto(cobordes[0][0], 1, construye_R(t)).copy()
muestra_matriz(operacion)
print(es_matriz_hadamard(operacion))
