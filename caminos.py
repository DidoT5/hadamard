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
    cobordes = [cambia_fila_i(c,j+1) for c,j in zip(cobordes, range(0,len(cobordes)))]
    # Creamos una lista de todas las posibles combinaciones de cobordes
    possible_comb = obtener_combinaciones_posibles(num_cobordes, t)
    matrices_hadamard = []
    for p in possible_comb:
        if len(p) < 2:
            coborde = cobordes[p[0]].copy()
            interseccion = calcula_numero_caminos_e_intersecciones(coborde.copy(),R.copy(), i, t)
            if interseccion == 0 and es_matriz_hadamard(np.multiply(coborde.copy(), R.copy()), t*4):
                matrices_hadamard.append((p[0]+2,coborde.copy()))

        elif type(p[1]) is tuple:
            if type(p[0]) is tuple:
                coborde_a = cobordes[p[0][0]].copy()
                for j in range(1,len(p[0])):
                    coborde_a = np.multiply(coborde_a.copy(),cobordes[0][j].copy())
            else:
                coborde_a = cobordes[p[0]].copy()
            coborde_b = cobordes[p[1][0]].copy()
            if len(p[1]) > 1:
                for j in range(1,len(p[1])):
                    coborde_b = np.multiply(coborde_b,cobordes[1][j].copy())
            num_caminos = calcula_numero_caminos_e_intersecciones(coborde_a, coborde_b, i, t)
            m_final = np.multiply(coborde_a.copy(), coborde_b.copy()).copy()
            num_intersecciones = calcula_numero_caminos_e_intersecciones(m_final, R, i, t)
            print("Conjunto a probar: ", p)
            print("Número de caminos e intersecciones: ",(num_caminos,num_intersecciones), " está en el cojunto:", (num_caminos,num_intersecciones) in sol_set)
            print("Es matriz de hadamard: ", es_matriz_hadamard(np.multiply(m_final.copy(), R.copy()), t*4))
            if ((num_caminos, num_intersecciones) in sol_set and es_matriz_hadamard(np.multiply(m_final.copy(), R.copy()), t*4)):
                matrices_hadamard.append((p, m_final.copy()))

        else:
            num_caminos = calcula_numero_caminos_e_intersecciones(cobordes[p[0]].copy(), cobordes[p[1]].copy(), i, t)
            m_final = np.multiply(cobordes[p[0]].copy(),cobordes[p[1]].copy())
            for j in range(2,len(p)):
                if calcula_numero_caminos_e_intersecciones(m_final.copy(), cobordes[p[j]].copy(), i, t) == num_caminos:
                    m_final = np.multiply(m_final.copy(),cobordes[p[j]].copy())
                else:
                    num_caminos = -1
                    break
            if num_caminos == -1:
                break
            elif ((num_caminos, calcula_numero_caminos_e_intersecciones(m_final.copy(), R.copy(), i, t)) in sol_set 
                and es_matriz_hadamard(np.multiply(m_final.copy(), R.copy()), t*4)):
                matrices_hadamard.append((p, m_final.copy()))

    return matrices_hadamard