import numpy as np
from sympy import *
from itertools import chain, combinations

def construye_R(t, dos_t, cuatro_t):
    matriz_R = np.ones( (cuatro_t, cuatro_t), dtype=np.int32)
    for i in range(1,dos_t):
        matriz_R[i,(dos_t-i):dos_t] = -1 
        matriz_R[i,(cuatro_t-i):cuatro_t] = -1
    for i in range(dos_t,cuatro_t):
        matriz_R[i,(i-dos_t+1):i+1] = -1
    return matriz_R.copy()

def es_matriz_hadamard(m, cuatro_t):
    return np.sum(m[1:cuatro_t,:])==0

def cambia_fila_i(m, i):
    m[i] = m[i]*(-1)
    return m.copy()

def calcula_numero_caminos_e_intersecciones(ma, mb, i, t):
    ac = 0
    for j in range(1,4*t):
        ac += ma[i,j] == mb[i,j] == -1
    return ac

def calcula_I_y_c(t, r_i):
    x, y = symbols('x, y', integer=True)

    eq = 2*x - 2*y - (2*t - r_i)
    #Preguntar porqué c no supera el valor 3 para poder parametrizarlo
    conds = [(0 <= x), (x < 4), (0 <= y)]

    # Resolver la ecuación diofantina en el parámetro z_0
    z, z_0 = symbols('z, z_0', integer=True)
    gensol = diophantine(eq, z, [x, y])
    ((xs, ys),) = gensol

    # Resolver las desigualdades para las restricciones en z_0
    conds_z = [cond.subs(x, xs).subs(y, ys) for cond in conds]
    conds_z_sol = solve(conds_z, z_0)

    #Encontrar el conjunto de soluciones finitas para los valores de z_0 
    set_z0 = (conds_z_sol.as_set() & Integers)
    sol_set = [(xs.subs(z_0, zi), ys.subs(z_0, zi)) for zi in set_z0]
    return sol_set

def clasifica_caminos(cobordes, i, t):
    # Calculo del parametro w
    num_cobordes = range(t-1,3*t-1)
    # Contruccion de R
    R = construye_R(t, t*2, t*4)
    # Calculo del parametro r_i
    r_i = np.sum(R[i,:]==-1)
    # Calculo de los valores c_i,I_i
    sol_set = calcula_I_y_c(t, r_i)
    # Actualiza la fila i de cada coborde i para tener dos -1
    cobordes = [cambia_fila_i(c,i+1) for c,i in zip(cobordes, range(0,len(cobordes)))]
    # Creamos una lista de todas las posibles combinaciones de cobordes
    possible_comb = []
    for x in num_cobordes:
        possible_comb += combinations(range(len(cobordes)),x)
    matrices_hadamard = []
    for p in possible_comb:
        if len(p) < 2:
            coborde = cobordes[p[0]]
            interseccion = calcula_numero_caminos_e_intersecciones(coborde.copy(),R.copy(), i, t)
            if interseccion == 0 and es_matriz_hadamard(np.multiply(coborde.copy(), R.copy()), t*4):
                matrices_hadamard.append((p[0]+2,coborde.copy()))

    return matrices_hadamard

'''
Hacer método para guardar las combinaciones que forman un i-camino con memoria,
es decir, crear un diccionario en el que se almacenan las combinaciones de matrices y la matriz con la que forman un i-camino
y una cola de posibles combinaciones de las que se eliminen los elementos reversos
Ejemplo: (m1,m2) == (m2,m1) -> Sólo se comprueba el primer literal

El número de intersecciones en i se define como la cantidad -1 que tienen en las mismas posiciones la matriz R y las combinaciones
de los cobordes
'''


    