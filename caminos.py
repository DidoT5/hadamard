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
        caminos_b = []
        #Conjunto a
        for c in comb[0]:
            coincidente = (c+i)%(2*t)
            if coincidente in comb[0]:
                pertence_camino = False
                for j in range(len(caminos_a)):
                    camino = caminos_a[j] 
                    if c == camino[-1]:
                        pertence_camino = True
                        if coincidente != camino[0]:
                            camino += [coincidente]
                        else:
                            camino += [coincidente]
                            ciclos.append(caminos_a.pop(j))
                if not pertence_camino:
                    caminos.append([c,coincidente])

            else:
                if all(c != camino[-1] for camino in caminos_a):
                    caminos_a.append([c])
        #Conjunto b
        for c in comb[1]:
            coincidente = (c+i)%(4*t)
            if coincidente in comb[0]:
                pertence_camino = False
                for j in range(len(caminos_b)):
                    camino = caminos_b[j] 
                    if c == camino[-1]:
                        pertence_camino = True
                        if coincidente != camino[0]:
                            camino += [coincidente]
                        else:
                            camino += [coincidente]
                            ciclos.append(caminos_b.pop(j))
                if not pertence_camino:
                    caminos.append([c,coincidente])

            else:
                if all(c != camino[-1] for camino in caminos_a):
                    caminos_b.append([c])
        caminos = caminos_a + caminos_b

    else:
        for c in comb:
            coincidente = (c+i)%(2*t) if c > 2*t else (c+i)%(2*t)
            # Si el coincidente esta en las combinaciones posibles
            if coincidente in comb:
                pertence_camino = False
                # Comprobamos si c forma parte de un camino (al estar ordenados solo miramos el ultimo indice)
                for j in range(len(caminos)):
                    camino = caminos[j] 
                    if c == camino[-1]:
                        pertence_camino = True
                        # Si el coincidente es igual al primer elemento forma un ciclo y hay que descartarlo de los caminos
                        if coincidente != camino[0]:
                            camino += [coincidente]
                        else:
                            camino += [coincidente]
                            ciclos.append(caminos.pop(j))
                if not pertence_camino:
                    caminos.append([c,coincidente])
            # Si ademas de no tener coincidentes, no forma parte de ningun camino, forma uno solo
            else:
                if all(c != camino[-1] for camino in caminos):
                    caminos.append([c])
    return (caminos, ciclos)

def es_fila_i_hadamard(c, I_i, t, r_i):
    return 2*c - 2*I_i - (2*t - r_i) == 0

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
    fila_i = cobordes[caminos[0][0]][i,:]
    c_i = len(caminos)
    for c in range(1,c_i):
        fila_i = np.multiply(fila_i,cobordes[c][i,:])
    I_i = calcula_intersecciones(fila_i, R[i,:], t)
    return es_fila_i_hadamard(c_i, I_i, t, r_i)