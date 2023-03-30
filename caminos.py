import numpy as np
import numexpr as ne
from sympy import *

def calcula_intersecciones(fila_i, R_i, t):
    ac = 0
    for j in range(1,4*t):
        ac += fila_i[j] == R_i[j] == -1
    return ac

def calcula_caminos_combinacion(comb, i, t):
    caminos_a = []
    ciclos_a = []
    caminos_b = []
    ciclos_b = []
    if type(len(comb[0])>0):
        #Conjunto a
        for c in comb[0]:
            coincidente = (c+i)%(2*t)
            if coincidente in comb[0]:
                pertence_camino = False
                for j in range(len(caminos_a)):
                    camino = caminos_a[j-len(ciclos_a)] 
                    if c == camino[-1]:
                        pertence_camino = True
                        if coincidente != camino[0]:
                            camino += [coincidente]
                        else:
                            ciclos_a.append(caminos_a.pop(j-len(ciclos_a)))
                if not pertence_camino:
                    caminos_a.append([c,coincidente])

            else:
                if all(c != camino[-1] for camino in caminos_a):
                    caminos_a.append([c])
    if (len(comb[1])>1):
        #Conjunto b
        for c in comb[1]:
            coincidente = (c+i)%(4*t)
            coincidente = coincidente if coincidente >= (2*t-1) else coincidente + 2*t -1
            if coincidente in comb[1]:
                pertence_camino = False
                for j in range(len(caminos_b)):
                    camino = caminos_b[j-len(ciclos_b)] 
                    if c == camino[-1]:
                        pertence_camino = True
                        if coincidente != camino[0]:
                            camino += [coincidente]
                        else:
                            ciclos_b.append(caminos_b.pop(j-len(ciclos_b)))
                if not pertence_camino:
                    caminos_b.append([c,coincidente])

            else:
                if all(c != camino[-1] for camino in caminos_b):
                    caminos_b.append([c])
    caminos = caminos_a + caminos_b
    ciclos = ciclos_a + ciclos_b
    return (caminos, ciclos)

def es_fila_i_hadamard(c, I_i, t, r_i):
    return (2*c - 2*I_i) - (2*t - r_i) == 0

def clasifica_caminos(comb, cobordes, i, r_i, t, R):
    (caminos, ciclos) = calcula_caminos_combinacion(comb, i, t)
    fila_i = np.ones(4*t, dtype = np.int32)
    c_i = len(caminos)
    for c in range(0,c_i):
        for cob in caminos[c]:
            producto = cobordes[cob][i,:]
            fila_i = ne.evaluate('fila_i*producto')
    I_i = calcula_intersecciones(fila_i, R[i,:], t)
    return es_fila_i_hadamard(c_i, I_i, t, r_i)