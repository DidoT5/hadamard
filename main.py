import numpy as np
from cobordes import genera_cobordes_espacio
from caminos import clasifica_caminos, obtener_combinaciones_posibles

t = 2

def muestra_matriz(m):
    for i in range(0,cuatro_t):
        print(m[i])

def construye_R(t, dos_t, cuatro_t):
    matriz_R = np.ones( (cuatro_t, cuatro_t), dtype=np.int32)
    for i in range(1,dos_t):
        matriz_R[i,(dos_t-i):dos_t] = -1 
        matriz_R[i,(cuatro_t-i):cuatro_t] = -1
    for i in range(dos_t,cuatro_t):
        matriz_R[i,(i-dos_t+1):i+1] = -1
    return matriz_R.copy()

def cambia_fila_i(m, i):
    m[i] = m[i]*(-1)
    return m.copy()

def obtiene_matriz_hadamard(t, comb, cobordes, r_i, R):
    if all (clasifica_caminos(comb, cobordes.copy(), i, r_i[i-1], t, R.copy()) for i in range(1,t)):
        return comb

def main(t):
    # Calculo del parametro w
    num_cobordes = range(t-1,3*t-1)
    # Creamos una lista de todas las posibles combinaciones de cobordes
    possible_comb = obtener_combinaciones_posibles(num_cobordes, t)
    print(len(possible_comb))
    # Contruccion de R
    R = construye_R(t, t*2, t*4)
    # Actualiza la fila i de cada coborde i para tener dos -1
    cobordes = genera_cobordes_espacio(t)
    cobordes = [cambia_fila_i(c,j+1) for c,j in zip(cobordes, range(0,len(cobordes)))]
    # Calculo del parametro r_i
    r_i = [np.sum(R[i,:]==-1) for i in range(1,t)]
    return [comb for comb in possible_comb if obtiene_matriz_hadamard(t, comb, cobordes, r_i, R)]
        
print(main(t))


