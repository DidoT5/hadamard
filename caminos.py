import numpy as np
from sympy import *
from itertools import chain, combinations

def calcula_intersecciones(fila_i, R_i, t):
    ac = 0
    for j in range(1,4*t):
        ac += fila_i[j] == R_i[j] == -1
    return ac

def calcula_caminos_combinacion(comb, i, t):
    caminos = []
    ciclos = []
    if type(comb[0]) is tuple:
        caminos_a = []
        ciclos_a = []
        caminos_b = []
        ciclos_b = []
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

    else:
        for c in comb:
            coincidente = 0
            if (c >= 2*t -1):
                coincidente = (c+i)%(4*t)
                coincidente = coincidente + 2*t-1 if coincidente < 2*t-1 else coincidente
            else:
                coincidente = (c+i)%(2*t)
            # Si el coincidente esta en las combinaciones posibles
            if coincidente in comb:
                pertence_camino = False
                # Comprobamos si c forma parte de un camino (al estar ordenados solo miramos el ultimo indice)
                for j in range(len(caminos)):
                    camino = caminos[j-len(ciclos)] 
                    if c == camino[-1]:
                        pertence_camino = True
                        # Si el coincidente es igual al primer elemento forma un ciclo y hay que descartarlo de los caminos
                        if coincidente != camino[0]:
                            camino += [coincidente]
                        else:
                            ciclos.append(caminos.pop(j-len(ciclos)))
                if not pertence_camino:
                    caminos.append([c,coincidente])
            # Si ademas de no tener coincidentes, no forma parte de ningun camino, forma uno solo
            else:
                if all(c != camino[-1] for camino in caminos):
                    caminos.append([c])
    return (caminos, ciclos)

def es_fila_i_hadamard(c, I_i, t, r_i):
    return (2*c - 2*I_i) - (2*t - r_i) == 0

def obtener_combinaciones_posibles(num_cobordes, t):
    possible_comb_a = []
    possible_comb_b = []
    total = []
    for x in num_cobordes:
        possible_comb_a += combinations(range(2*t-1),x)
    for x in num_cobordes:
        possible_comb_b += combinations(range(2*t-1,4*t-3),x)
    total += possible_comb_a + possible_comb_b
    for a in possible_comb_a:
        for b in possible_comb_b:
            if len(a) + len(b) < num_cobordes[-1]+1:
                total.append((a,b))
    
    return total

def clasifica_caminos(comb, cobordes, i, r_i, t, R):
    (caminos, ciclos) = calcula_caminos_combinacion(comb, i, t)
    fila_i = np.ones(4*t, dtype = np.int32)
    c_i = len(caminos)
    for c in range(0,c_i):
        for cob in caminos[c]:
            fila_i = np.multiply(fila_i,cobordes[cob][i,:])
    I_i = calcula_intersecciones(fila_i, R[i,:], t)
    return es_fila_i_hadamard(c_i, I_i, t, r_i)