import numpy as np

def genera_cobordes(t, i):
    
    i = i-1
    cuatro_t = 4*t
    dos_t = 2*t
    matriz_base = np.ones( (cuatro_t, cuatro_t), dtype=np.int32)

    if i < dos_t:
        for j in range(1,cuatro_t):
            fila_base = np.ones(cuatro_t, dtype = np.int32)

            if j < i :
                fila_base[i-j] = -1                 
                fila_base[i] = -1

            elif j == i :
                fila_base[1:i] = -1                 
                fila_base[i+1:cuatro_t] = -1

            elif j > i and j < dos_t :
                fila_base[i] = -1                 
                fila_base[dos_t-(j-i)] = -1

            elif j >= dos_t and j <= (dos_t + i - 1):
                fila_base[i] = -1                 
                fila_base[cuatro_t+j-dos_t-i] = -1

            else :
                fila_base[i] = -1                 
                fila_base[j-i] = -1
            
            matriz_base[j] = fila_base.copy()
    else:
        for j in range(1,cuatro_t):
            fila_base = np.ones(cuatro_t, dtype = np.int32)
            if j <= i - dos_t :
                fila_base[i-j] = -1                 
                fila_base[i] = -1

            elif j > i - dos_t and j <= dos_t - 1:
                fila_base[i] = -1                 
                fila_base[cuatro_t - (j + dos_t - i)] = -1

            elif j > dos_t -1 and j < i:
                fila_base[i] = -1                 
                fila_base[cuatro_t+j-dos_t-i] = -1

            elif j == i :
                fila_base[1:i] = -1                 
                fila_base[i+1:cuatro_t] = -1

            else :
                fila_base[i] = -1                 
                fila_base[j-i] = -1
            
            matriz_base[j] = fila_base.copy()

    return matriz_base

def genera_cobordes_espacio(t):
    conjunto_a = []
    conjunto_b = []
    for i in range(2, t*2):
        conjunto_a.append(genera_cobordes(t, i).copy())
    for i in range(t*2, (t*4)-1):
        conjunto_b.append(genera_cobordes(t, i).copy())
    return conjunto_a + conjunto_b